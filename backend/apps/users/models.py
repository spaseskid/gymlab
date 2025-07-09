from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    """Custom user model for gym members."""
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('coach', 'Coach'),
        ('employee', 'Employee'),
    ]

    # Personal info
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    member_id = models.CharField(max_length=10, unique=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    gender = models.CharField(
        max_length=20,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('prefer_not_to_say', 'Prefer not to say'),
        ],
        null=True,
        blank=True
    )

    # Physical stats
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
    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True, help_text="cm")
    weight = models.FloatField(null=True, blank=True, help_text="kg")
    # Measurements
    measurements_bicep = models.PositiveIntegerField(blank=True, null=True, help_text="cm")
    measurements_forearm = models.PositiveIntegerField(blank=True, null=True, help_text="cm")
    measurements_shoulder = models.PositiveIntegerField(blank=True, null=True, help_text="cm")
    measurements_chest = models.PositiveIntegerField(blank=True, null=True, help_text="cm")
    measurements_waist = models.PositiveIntegerField(blank=True, null=True, help_text="cm")
    measurements_hips = models.PositiveIntegerField(blank=True, null=True, help_text="cm")
    measurements_calves = models.PositiveIntegerField(blank=True, null=True, help_text="cm")

    goal = models.ManyToManyField('users.Goal', related_name='users',blank=True)


    next_workout_type = models.CharField(
        max_length=10,
        choices=[('push', 'Push'), ('pull', 'Pull'), ('legs', 'Legs')],
        default='push'
    )

    SUBSCRIPTION_CHOICES = [
        ('1_month', '1 Month'),
        ('3_months', '3 Months'),
        ('6_months', '6 Months'),
    ]

    SUBSCRIPTION_DURATIONS = {
        '1_month': 30,
        '3_months': 90,
        '6_months': 180,
    }

    subscription_type = models.CharField(
        max_length=20,
        choices=SUBSCRIPTION_CHOICES,
        null=True,
        blank=True
    )
    subscription_start = models.DateField(null=True, blank=True)
    subscription_end = models.DateField(null=True, blank=True)

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='member'
    )

    def save(self, *args, **kwargs):
        # Sync custom names with Django's built-in ones
        self.first_name = self.name
        self.last_name = self.surname

        # Generate member ID if not set
        if not self.member_id:
            self.member_id = self.generate_member_id()

        # Auto-fill subscription dates if type selected
        if self.subscription_type:
            today = timezone.now().date()
            if not self.subscription_start:
                self.subscription_start = today
            if not self.subscription_end:
                duration = self.SUBSCRIPTION_DURATIONS.get(self.subscription_type)
                self.subscription_end = self.subscription_start + timezone.timedelta(days=duration)

        super().save(*args, **kwargs)

    def generate_member_id(self):
        """Generate unique member ID in format C000001"""
        last_user = User.objects.filter(member_id__startswith='C').order_by('member_id').last()
        if last_user and last_user.member_id:
            last_number = int(last_user.member_id[1:])
            new_number = last_number + 1
        else:
            new_number = 1
        return f"C{new_number:06d}"

    def has_active_subscription(self):
        """Check if the subscription is currently active."""
        return (
                self.subscription_end is not None and
                self.subscription_end >= timezone.now().date()
        )

    def days_remaining(self):
        """Return how many days are left in the subscription."""
        if not self.subscription_end:
            return 0
        remaining = (self.subscription_end - timezone.now().date()).days
        return max(0, remaining)

    def advance_workout_cycle(self):
        """Move to next workout in the cycle: push -> pull -> legs -> push"""
        cycle = {'push': 'pull', 'pull': 'legs', 'legs': 'push'}
        self.next_workout_type = cycle.get(self.next_workout_type, 'push')
        self.save()

    def __str__(self):
        return f"{self.name} {self.surname} ({self.member_id})"


class Goal(models.Model):
    key = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
