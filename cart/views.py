from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Cart, CartItem
from courses.models import Course, Enrollment


def get_or_create_cart(user):
    """Get or create cart for user."""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_view(request):
    """Display shopping cart."""
    cart = get_or_create_cart(request.user)
    cart_items = cart.items.all().select_related('course')
    total = cart.get_total()
    
    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def add_to_cart(request, course_id):
    """Add course to cart."""
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    # Check if user already owns the course
    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.error(request, 'Você já possui este curso.')
        return redirect('acquire_courses')
    
    # Get or create cart
    cart = get_or_create_cart(request.user)
    
    # Check if course is already in cart
    if CartItem.objects.filter(cart=cart, course=course).exists():
        messages.info(request, 'Este curso já está no carrinho.')
    else:
        CartItem.objects.create(cart=cart, course=course)
        messages.success(request, f'{course.name} adicionado ao carrinho!')
    
    return redirect('acquire_courses')


@login_required
def remove_from_cart(request, course_id):
    """Remove course from cart."""
    cart = get_or_create_cart(request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, course_id=course_id)
    course_name = cart_item.course.name
    cart_item.delete()
    
    messages.success(request, f'{course_name} removido do carrinho.')
    return redirect('cart')
