from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
import random
import string
import uuid


class CustomUserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom user model with email as the username field."""
    
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Profile(models.Model):
    """User profile with additional information."""
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Data de Nascimento')
    nationality = models.CharField(max_length=100, blank=True, verbose_name='Nacionalidade')
    
    def __str__(self):
        return f'Profile of {self.user.email}'
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class EmailVerificationCode(models.Model):
    """Email verification code for email change requests."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='email_verification_codes'
    )
    new_email = models.EmailField(verbose_name='New Email')
    code = models.CharField(max_length=6, verbose_name='Verification Code')
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Verification code for {self.user.email} -> {self.new_email}'
    
    def is_valid(self):
        """Check if the code is still valid (not expired and not used)."""
        if self.is_used:
            return False
        expiry_minutes = getattr(settings, 'EMAIL_VERIFICATION_EXPIRY', 10)
        expiry_time = self.created_at + timedelta(minutes=expiry_minutes)
        return timezone.now() < expiry_time
    
    @staticmethod
    def generate_code():
        """Generate a random 6-digit verification code."""
        return ''.join(random.choices(string.digits, k=6))
    
    class Meta:
        verbose_name = 'Email Verification Code'
        verbose_name_plural = 'Email Verification Codes'
        ordering = ['-created_at']


class PasswordResetCode(models.Model):
    """Password reset code for forgot password functionality."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='password_reset_codes'
    )
    code = models.CharField(max_length=6, verbose_name='Verification Code')
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Password reset code for {self.user.email}'
    
    def is_valid(self):
        """Check if the code is still valid (not expired and not used)."""
        if self.is_used:
            return False
        expiry_minutes = getattr(settings, 'PASSWORD_RESET_EXPIRY_MINUTES', 10)
        expiry_time = self.created_at + timedelta(minutes=expiry_minutes)
        return timezone.now() < expiry_time
    
    @staticmethod
    def generate_code():
        """Generate a random 6-digit verification code."""
        return ''.join(random.choices(string.digits, k=6))
    
    class Meta:
        verbose_name = 'Password Reset Code'
        verbose_name_plural = 'Password Reset Codes'
        ordering = ['-created_at']
