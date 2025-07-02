from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.


User = get_user_model()

class Exercise(models.Model):
    CATEGORY_CHOICES = [
        ('push', 'Push'),
        ('pull', 'Pull'),
        ('legs', 'Legs'),
    ]
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=200)
    youtube_link = models.URLField(blank=True)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reps = models.PositiveIntegerField(null=True, blank=True, help_text="Reps for the current exercise")
    duration = models.DurationField(null=True, blank=True, help_text="Optional exercise duration (e.g., 00:05:00 for 5 minutes)")
    program_level =models.CharField(
        max_length=20,
        choices=[
            ('beg', 'Beginner'),
            ('adv', 'Advanced'),
            ('pro', 'Professional'),
        ],
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['category', 'order', 'name']
        constraints = [
            models.UniqueConstraint(fields=['category', 'program_level', 'order'], name='unique_order_per_category_level')
        ]
    def __str__(self):
        return f"{self.get_category_display()} - {self.name}"



class WorkoutSession(models.Model):
    """Track completed workout sessions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_sessions')
    workout_type = models.CharField(
        max_length=10,
        choices=[('push', 'Push'), ('pull', 'Pull'), ('legs', 'Legs')]
    )
    program_level = models.CharField(   # optional, store user program level at time of workout
        max_length=20,
        choices=[
            ('beg', 'Beginner'),
            ('adv', 'Advanced'),
            ('pro', 'Professional'),
        ],
        null=True,
        blank=True
    )
    completed_date = models.DateTimeField(default=timezone.now)
    duration = models.DurationField(null=True, blank=True, help_text="Total workout duration")
    exercises_completed = models.ManyToManyField(Exercise, blank=True, related_name='workout_sessions')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-completed_date']
        indexes = [
            models.Index(fields=['user', 'completed_date']),
        ]

    def __str__(self):
        return f"{self.user.name} - {self.get_workout_type_display()} on {self.completed_date.strftime('%Y-%m-%d')}"