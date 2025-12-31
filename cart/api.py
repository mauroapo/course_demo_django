from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from courses.models import Course, Enrollment


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart_api(request):
    """API endpoint to add course to cart."""
    course_id = request.data.get('course_id')
    
    if not course_id:
        return Response({'error': 'course_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        course = Course.objects.get(id=course_id, is_active=True)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if user already owns the course
    if Enrollment.objects.filter(user=request.user, course=course).exists():
        return Response({'error': 'You already own this course'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get or create cart
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    # Check if course is already in cart
    if CartItem.objects.filter(cart=cart, course=course).exists():
        return Response({'message': 'Course already in cart'}, status=status.HTTP_200_OK)
    
    # Add to cart
    CartItem.objects.create(cart=cart, course=course)
    
    return Response({
        'message': 'Course added to cart',
        'cart_item_count': cart.get_item_count()
    }, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart_api(request, course_id):
    """API endpoint to remove course from cart."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    try:
        cart_item = CartItem.objects.get(cart=cart, course_id=course_id)
        cart_item.delete()
        return Response({
            'message': 'Course removed from cart',
            'cart_item_count': cart.get_item_count()
        }, status=status.HTTP_200_OK)
    except CartItem.DoesNotExist:
        return Response({'error': 'Course not in cart'}, status=status.HTTP_404_NOT_FOUND)
