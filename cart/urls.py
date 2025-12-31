from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/<int:course_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:course_id>/', views.remove_from_cart, name='remove_from_cart'),
]
