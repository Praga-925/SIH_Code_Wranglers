from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for User model with role field
    """
    # Fields to display in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active', 'date_joined')
    
    # Fields to filter by in the admin sidebar
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    # Fields to search in the admin search box
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Order by username
    ordering = ('username',)
    
    # Fields to show when editing a user
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )
    
    # Fields to show when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )


# Register the custom User model with the custom admin
admin.site.register(User, CustomUserAdmin)
