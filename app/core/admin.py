from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = [
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_staff',
                    'is_active',
                    'is_superuser',
                )
            }
        ),
        (
            _('Important Dates'),
            {
                'fields': ('last_login',)
            }
        )]
    readonly_fields = ['last_login']
    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        })]


class OrderAdmin(admin.ModelAdmin):
    """Define the admin page for Orders."""
    ordering = ['id']
    list_display = ['id', 'order_type', 'created_date', 'status', 'total_amount']
    fieldsets = [
        (None, {
                'fields': (
                    'user',
                    'order_type',
                    'quantity',
                    'total_amount',
                    'status',
                )
            }
        ),
        (
            _('Important Dates'),
            {
                'fields': ('created_date', 'last_modified',)
            }
        )]
    readonly_fields = ['last_modified', 'created_date']
    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': (
                'user',
                'order_type',
                'quantity',
                'total_amount',
            )
        })]


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Order, OrderAdmin)
