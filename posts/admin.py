from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()  # This ensures you're using your custom user model

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active','get_groups']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'email']

    # Remove password field
    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    def get_groups(self, obj):
        """Display the groups the user is a part of in list view"""
        return ", ".join([group.name for group in obj.groups.all()])
    get_groups.short_description = 'Groups'

# Register the custom user model and the custom admin class
admin.site.register(User, CustomUserAdmin)
