from django.db import models
from django.conf import settings
from courses.models import Course


class Organization(models.Model):
    """Organization for B2B course packages."""
    
    name = models.CharField(max_length=200, verbose_name='Nome')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        ordering = ['name']


class OrgMember(models.Model):
    """Organization member."""
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('member', 'Member'),
    ]
    
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='members'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='org_memberships'
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.email} - {self.organization.name} ({self.role})'
    
    class Meta:
        verbose_name = 'Organization Member'
        verbose_name_plural = 'Organization Members'
        unique_together = ['organization', 'user']


class OrgPackage(models.Model):
    """Course package for organizations."""
    
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='packages'
    )
    name = models.CharField(max_length=200, verbose_name='Nome')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    seat_count = models.PositiveIntegerField(verbose_name='Número de Vagas')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    
    def __str__(self):
        return f'{self.name} - {self.organization.name}'
    
    class Meta:
        verbose_name = 'Organization Package'
        verbose_name_plural = 'Organization Packages'


class OrgPackageItem(models.Model):
    """Course included in an organization package."""
    
    org_package = models.ForeignKey(
        OrgPackage,
        on_delete=models.CASCADE,
        related_name='items'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return f'{self.course.name} in {self.org_package.name}'
    
    class Meta:
        verbose_name = 'Organization Package Item'
        verbose_name_plural = 'Organization Package Items'
        unique_together = ['org_package', 'course']


class OrgSeatAssignment(models.Model):
    """Assignment of a course seat to a user in an organization."""
    
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='seat_assignments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )
    assigned_to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='org_seat_assignments'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.course.name} -> {self.assigned_to_user.email} ({self.organization.name})'
    
    class Meta:
        verbose_name = 'Organization Seat Assignment'
        verbose_name_plural = 'Organization Seat Assignments'
        unique_together = ['organization', 'course', 'assigned_to_user']
