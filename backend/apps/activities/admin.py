from django.contrib import admin
from .models import ExtraActivity, ExtraActivityRegistration

# Register your models here.
@admin.register(ExtraActivity)
class ExtraActivityAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'day_of_week', 'start_time', 'duration',
        'capacity', 'program_level', 'coach', 'registered_count', 'waiting_list_count'
    )
    list_filter = ('day_of_week', 'program_level', 'coach')
    search_fields = ('title', 'description')
    ordering = ('day_of_week', 'start_time')
    readonly_fields = ('registered_count', 'waiting_list_count')


@admin.register(ExtraActivityRegistration)
class ExtraActivityRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity', 'registered_at', 'waiting')
    list_filter = ('waiting', 'registered_at')
    search_fields = ('user__name', 'user__surname', 'activity__title')
    ordering = ('-registered_at',)


