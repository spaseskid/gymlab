from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.

User = get_user_model()

class ExtraActivity(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_time = models.TimeField()
    duration = models.PositiveIntegerField(null=True, blank=True, help_text="Total activity duration in minutes")
    capacity = models.PositiveIntegerField(default=40)
    coach = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'coach'})
    day_of_week = models.CharField(
        max_length=10,
        choices=[('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'),
                 ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday')]
    )
    program_level = models.CharField(   # optional, store user program level at time of workout
        max_length=20,
        choices=[
            ('beg', 'Beginner'),('adv', 'Advanced'),('pro', 'Professional'),],
        null=True,
        blank=True
    )
    def registered_count(self):
        return self.registrations.filter(waiting=False).count()

    def waiting_list_count(self):
        return self.registrations.filter(waiting=True).count()

    def __str__(self):
        return f"{self.title} ({self.day_of_week.capitalize()} at {self.start_time})"


class ExtraActivityRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(ExtraActivity, related_name="registrations", on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    waiting = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'activity')
        ordering = ['activity__day_of_week', 'activity__start_time']

    def __str__(self):
        return f"{self.user} - {self.activity} ({'Waiting' if self.waiting else 'Confirmed'})"
