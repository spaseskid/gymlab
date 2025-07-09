from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import *
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'surname', 'email', 'phone_number', 'image', 'gender')}),
        (_('Membership'), {
            'fields': (
                'member_id', 'role', 'subscription_type', 'subscription_start', 'subscription_end',
                'goal', 'next_workout_type'
            ), 'classes': ('collapse',)
        }),
        (_('Physical Stats'), {'fields': ('age', 'height', 'weight', 'program_level'), 'classes': ('collapse',)}),
        (_('Measurements'), {
            'fields': (
                'measurements_bicep', 'measurements_forearm', 'measurements_shoulder',
                'measurements_chest', 'measurements_waist', 'measurements_hips', 'measurements_calves'
            ), 'classes': ('collapse',)
        }),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'), 'classes': ('collapse',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined'), 'classes': ('collapse',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'name', 'surname','subscription_type'),
        }),
    )

    list_display = ('member_id','username', 'name', 'surname', 'phone_number', 'subscription_status', 'subscription_end','role')
    list_filter = ('role', 'program_level', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'name', 'surname', 'phone_number', 'member_id')
    ordering = ('member_id',)

    def subscription_status(self, obj):
        if obj.role == 'employee' or obj.role == 'coach':
            return format_html(
                '<span style="color: green;text-align: center">✓</span>',
            )
        if obj.has_active_subscription():
            return format_html(
                '<span style="color: green; text-align:center">✓ Active until {}</span>',
                obj.subscription_end.strftime('%Y-%m-%d')
            )

        return format_html('<span style="color: red; text-align:center">✗ No active subscription</span>')

    subscription_status.short_description = "Subscription"


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('key', 'name')

admin.site.unregister(Group)