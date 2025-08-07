# Path: /accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Company, Applicant

class UserAdmin(BaseUserAdmin):
    """
    Defines a custom admin panel for our User model.
    This fixes the issue where saving a user requires re-entering a password.
    """
    # These are the fields displayed when viewing a list of users
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    # These fields can be used to filter the user list
    list_filter = ('is_staff', 'is_active', 'user_type')
    # These are the fields available for searching
    search_fields = ('username', 'email')
    # This controls the ordering of users
    ordering = ('username',)

    # This is the most important part. It organizes the fields on the user edit page.
    # We keep the 'password' field in a separate section. The form knows how to handle it correctly.
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom Fields', {'fields': ('user_type', 'email_verified')}),
    )

# Unregister the default User admin if it's registered
# admin.site.unregister(User)

# Register our custom User admin
admin.site.register(User, UserAdmin)
admin.site.register(Company)
admin.site.register(Applicant)