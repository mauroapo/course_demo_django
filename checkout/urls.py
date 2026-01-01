from django.urls import path
from . import views

urlpatterns = [
    # Checkout pages
    path('', views.free_checkout, name='checkout'),
    # path('pix/', views.checkout_pix, name='checkout_pix'),
    
    # Payment status
    # path('success/<int:order_id>/', views.payment_success, name='payment_success'),
    # path('cancel/', views.payment_cancel, name='payment_cancel'),
    # path('check-status/<int:order_id>/', views.check_payment_status, name='check_payment_status'),
    
    # Webhook
    # path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    
    # Legacy URLs (backward compatibility)
    path('process/', views.process_checkout, name='process_checkout'),
    path('success/', views.checkout_success, name='checkout_success'),
]
