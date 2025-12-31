from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
import stripe
import json

from cart.models import Cart
from courses.models import Enrollment
from .models import Order, OrderItem
from . import stripe_utils


@login_required
def checkout_view(request):
    """Display checkout page with payment options."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all().select_related('course')
    total = cart.get_total()
    
    if not cart_items:
        messages.warning(request, 'Seu carrinho está vazio.')
        return redirect('cart')
    
    # Create payment intent for this checkout
    try:
        amount_cents = stripe_utils.convert_to_cents(total)
        
        # Create payment intent
        payment_intent = stripe_utils.create_payment_intent(
            amount=amount_cents,
            currency='brl',
            payment_method_types=['card'],
            metadata={
                'user_id': request.user.id,
                'user_email': request.user.email,
            }
        )
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            currency='BRL',
            stripe_payment_intent_id=payment_intent.id,
            payment_method='credit_card',
            payment_status='pending'
        )
        
        # Create order items from cart
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                course=cart_item.course,
                price=cart_item.course.price
            )
        
        # Clear cart immediately after creating order
        cart.items.all().delete()
        
        context = {
            'cart_items': list(order.items.all().select_related('course')),  # Use order items instead
            'total': total,
            'order': order,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
            'client_secret': payment_intent.client_secret,
        }
        
        return render(request, 'checkout/checkout.html', context)
        
    except Exception as e:
        messages.error(request, f'Erro ao processar checkout: {str(e)}')
        return redirect('cart')


@login_required
def checkout_pix(request):
    """Create PIX payment."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all().select_related('course')
    total = cart.get_total()
    
    if not cart_items:
        messages.warning(request, 'Seu carrinho está vazio.')
        return redirect('cart')
    
    try:
        amount_cents = stripe_utils.convert_to_cents(total)
        
        # Create PIX payment intent
        payment_intent = stripe_utils.create_pix_payment(
            amount=amount_cents,
            currency='brl',
            metadata={
                'user_id': request.user.id,
                'user_email': request.user.email,
            }
        )
        
        # Get PIX details
        pix_details = stripe_utils.get_pix_details(payment_intent.id)
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            currency='BRL',
            stripe_payment_intent_id=payment_intent.id,
            payment_method='pix',
            payment_status='pending',
            pix_qr_code=pix_details.get('qr_code') if pix_details else None,
            pix_code=pix_details.get('code') if pix_details else None
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                course=cart_item.course,
                price=cart_item.course.price
            )
        
        context = {
            'order': order,
            'pix_details': pix_details,
            'total': total,
        }
        
        return render(request, 'checkout/pix.html', context)
        
    except Exception as e:
        messages.error(request, f'Erro ao criar pagamento PIX: {str(e)}')
        return redirect('cart')


@login_required
def payment_success(request, order_id):
    """Display payment success page."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Check if payment is successful
    if order.payment_status != 'succeeded':
        messages.warning(request, 'Pagamento ainda não confirmado.')
        return redirect('my_courses')
    
    return render(request, 'checkout/success.html', {'order': order})


@login_required
def payment_cancel(request):
    """Handle cancelled payments."""
    messages.info(request, 'Pagamento cancelado. Você pode tentar novamente.')
    return redirect('cart')


# @csrf_exempt
# @require_POST
# def stripe_webhook(request):
#     """Handle Stripe webhooks."""
#     payload = request.body
#     sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
#     print("=" * 50)
#     print("STRIPE WEBHOOK RECEIVED")
#     print("=" * 50)
    
#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
#         )
#         print(f"Event Type: {event['type']}")
#         print(f"Event ID: {event['id']}")
#     except ValueError as e:
#         print(f"Invalid payload: {e}")
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         print(f"Invalid signature: {e}")
#         return HttpResponse(status=400)
    
#     # Handle the event
#     if event['type'] == 'payment_intent.succeeded':
#         payment_intent = event['data']['object']
#         print(f"Payment Intent ID: {payment_intent['id']}")
#         print(f"Amount: {payment_intent['amount']}")
#         handle_payment_success(payment_intent)
    
#     elif event['type'] == 'payment_intent.payment_failed':
#         payment_intent = event['data']['object']
#         print(f"Payment Failed - Intent ID: {payment_intent['id']}")
#         handle_payment_failed(payment_intent)
    
#     else:
#         print(f"Unhandled event type: {event['type']}")
    
#     return HttpResponse(status=200)


@transaction.atomic
def handle_payment_success(payment_intent):
    """Handle successful payment - enroll user in courses."""
    payment_intent_id = payment_intent['id']
    
    print(f"Handling payment success for: {payment_intent_id}")
    
    try:
        order = Order.objects.get(stripe_payment_intent_id=payment_intent_id)
        print(f"Found Order #{order.id} for user {order.user.email}")
        
        # Update order status
        order.payment_status = 'succeeded'
        order.save()
        print(f"Order #{order.id} marked as succeeded")
        
        # Create enrollments
        enrollments_created = 0
        for item in order.items.all():
            enrollment, created = Enrollment.objects.get_or_create(
                user=order.user,
                course=item.course,
                defaults={'source': 'individual'}
            )
            if created:
                enrollments_created += 1
                print(f"✓ Enrolled user in: {item.course.name}")
            else:
                print(f"- User already enrolled in: {item.course.name}")
        
        print(f"Total enrollments created: {enrollments_created}")
        print("Payment success handled successfully!")
            
    except Order.DoesNotExist:
        print(f"ERROR: Order not found for payment_intent_id: {payment_intent_id}")
    except Exception as e:
        print(f"ERROR handling payment success: {str(e)}")
        import traceback
        traceback.print_exc()


def handle_payment_failed(payment_intent):
    """Handle failed payment."""
    try:
        order = Order.objects.get(stripe_payment_intent_id=payment_intent.id)
        order.payment_status = 'failed'
        order.save()
    except Order.DoesNotExist:
        pass


@login_required
def check_payment_status(request, order_id):
    """Check payment status (for PIX polling)."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    try:
        status = stripe_utils.get_payment_status(order.stripe_payment_intent_id)
        
        if status == 'succeeded' and order.payment_status != 'succeeded':
            order.payment_status = 'succeeded'
            order.save()
            
            # Create enrollments
            for item in order.items.all():
                Enrollment.objects.get_or_create(
                    user=order.user,
                    course=item.course,
                    defaults={'source': 'individual'}
                )
            
            # Clear cart
            cart = Cart.objects.filter(user=order.user).first()
            if cart:
                cart.items.all().delete()
        
        return JsonResponse({
            'status': order.payment_status,
            'is_paid': order.is_paid
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# Legacy view for backward compatibility
@login_required
@transaction.atomic
def process_checkout(request):
    """Redirect to new checkout flow."""
    return redirect('checkout')


@login_required
def checkout_success(request):
    """Legacy success page - redirect to my courses."""
    return redirect('my_courses')
