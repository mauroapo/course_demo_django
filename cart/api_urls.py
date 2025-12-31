from django.urls import path
from . import api

urlpatterns = [
    path('cart/items/', api.add_to_cart_api, name='api_add_to_cart'),
    path('cart/items/<int:course_id>/', api.remove_from_cart_api, name='api_remove_from_cart'),
]
