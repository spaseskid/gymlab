from django.contrib import admin
from .models import Exercise, WorkoutSession

# Register your models here.


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'program_level', 'order', 'is_active')
    list_filter = ('category', 'program_level', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('category', 'program_level', )


@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'workout_type', 'program_level', 'completed_date', 'duration')
    list_filter = ('workout_type', 'program_level', 'completed_date')
    search_fields = ('user__name', 'user__surname', 'notes')
    date_hierarchy = 'completed_date'
