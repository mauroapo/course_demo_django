from django.db import models
from django.conf import settings
from courses.models import Course


class Cart(models.Model):
    """Shopping cart for a user."""
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Cart of {self.user.email}'
    
    def get_total(self):
        """Calculate total price of items in cart."""
        return sum(item.course.price for item in self.items.all())
    
    def get_item_count(self):
        """Get number of items in cart."""
        return self.items.count()
    
    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class CartItem(models.Model):
    """Item in a shopping cart."""
    
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.course.name} in cart of {self.cart.user.email}'
    
    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = ['cart', 'course']
        ordering = ['-added_at']
