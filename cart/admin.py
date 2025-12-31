from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin configuration for Cart."""
    
    list_display = ('user', 'created_at', 'updated_at', 'get_item_count')
    search_fields = ('user__email',)
    readonly_fields = ('created_at', 'updated_at')
    
    def get_item_count(self, obj):
        return obj.get_item_count()
    get_item_count.short_description = 'Items'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin configuration for CartItem."""
    
    list_display = ('cart', 'course', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('cart__user__email', 'course__name')
    readonly_fields = ('added_at',)
