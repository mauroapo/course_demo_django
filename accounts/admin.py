from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Profile, EmailVerificationCode, PasswordResetCode


class ProfileInline(admin.StackedInline):
    """Inline admin for Profile."""
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile Information'
    fields = ('date_of_birth', 'nationality')


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Admin configuration for CustomUser."""
    
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    inlines = (ProfileInline,)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for Profile."""
    
    list_display = ('user', 'date_of_birth', 'nationality')
    search_fields = ('user__email', 'nationality')
    list_filter = ('nationality',)


@admin.register(EmailVerificationCode)
class EmailVerificationCodeAdmin(admin.ModelAdmin):
    """Admin configuration for EmailVerificationCode."""
    
    list_display = ('user', 'new_email', 'code', 'created_at', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__email', 'new_email', 'code')
    readonly_fields = ('created_at',)


@admin.register(PasswordResetCode)
class PasswordResetCodeAdmin(admin.ModelAdmin):
    """Admin configuration for PasswordResetCode."""
    
    list_display = ('user', 'code', 'created_at', 'is_used', 'is_valid_status')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__email', 'code')
    readonly_fields = ('code', 'created_at')
    ordering = ('-created_at',)
    
    def is_valid_status(self, obj):
        """Display if code is currently valid."""
        return obj.is_valid()
    is_valid_status.short_description = 'Valid'
    is_valid_status.boolean = True
