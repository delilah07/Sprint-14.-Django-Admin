
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_active',
        'is_staff',
        'is_superuser',
    )

    list_display_links = ('id', 'email')

    list_filter = (
        'role',
        'is_active',
        'is_staff',
        'is_superuser',
    )

    search_fields = (
        '=id',
        'email',
        'first_name',
        'last_name',
        'middle_name',
    )

    ordering = ('id',)
    list_per_page = 20

    fieldsets = (
        ('Account information', {
            'fields': ('email', 'password'),
        }),
        ('Personal information', {
            'fields': ('first_name', 'middle_name', 'last_name'),
        }),
        ('Library role', {
            'fields': ('role',),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        ('Dates', {
            'fields': ('last_login', 'created_at', 'updated_at'),
        }),
    )

    readonly_fields = ('last_login', 'created_at', 'updated_at')

    filter_horizontal = ()
