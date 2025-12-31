def cart_item_count(request):
    """Context processor to add cart item count to all templates."""
    if request.user.is_authenticated:
        from .models import Cart
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return {'cart_item_count': cart.get_item_count()}
    return {'cart_item_count': 0}
