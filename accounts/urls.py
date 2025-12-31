from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_view, name='account'),
    path('account/change-email/', views.change_email_request, name='change_email_request'),
    path('account/change-email/confirm/', views.change_email_confirm, name='change_email_confirm'),
    
    # Password reset (3-step flow)
    path('forgot-password/', views.forgot_password_request, name='forgot_password_request'),
    path('forgot-password/verify/', views.forgot_password_verify, name='forgot_password_verify'),
    path('forgot-password/reset/', views.forgot_password_reset, name='forgot_password_reset'),
]
