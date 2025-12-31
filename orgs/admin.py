from django.contrib import admin
from .models import Organization, OrgMember, OrgPackage, OrgPackageItem, OrgSeatAssignment


class OrgMemberInline(admin.TabularInline):
    model = OrgMember
    extra = 1


class OrgPackageInline(admin.TabularInline):
    model = OrgPackage
    extra = 0


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Admin configuration for Organization."""
    
    list_display = ('name', 'created_at', 'member_count')
    search_fields = ('name',)
    inlines = [OrgMemberInline, OrgPackageInline]
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'


@admin.register(OrgMember)
class OrgMemberAdmin(admin.ModelAdmin):
    """Admin configuration for OrgMember."""
    
    list_display = ('user', 'organization', 'role', 'joined_at')
    list_filter = ('role', 'joined_at')
    search_fields = ('user__email', 'organization__name')


class OrgPackageItemInline(admin.TabularInline):
    model = OrgPackageItem
    extra = 1


@admin.register(OrgPackage)
class OrgPackageAdmin(admin.ModelAdmin):
    """Admin configuration for OrgPackage."""
    
    list_display = ('name', 'organization', 'price', 'seat_count', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'organization__name')
    inlines = [OrgPackageItemInline]


@admin.register(OrgPackageItem)
class OrgPackageItemAdmin(admin.ModelAdmin):
    """Admin configuration for OrgPackageItem."""
    
    list_display = ('org_package', 'course')
    search_fields = ('org_package__name', 'course__name')


@admin.register(OrgSeatAssignment)
class OrgSeatAssignmentAdmin(admin.ModelAdmin):
    """Admin configuration for OrgSeatAssignment."""
    
    list_display = ('organization', 'course', 'assigned_to_user', 'assigned_at')
    list_filter = ('assigned_at',)
    search_fields = ('organization__name', 'course__name', 'assigned_to_user__email')
