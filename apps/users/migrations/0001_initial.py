# Generated by Django 5.2.3 on 2025-07-01 22:54

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('member_id', models.CharField(blank=True, max_length=10, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('prefer_not_to_say', 'Prefer not to say')], max_length=20, null=True)),
                ('program_level', models.CharField(blank=True, choices=[('beg', 'Beginner'), ('adv', 'Advanced'), ('pro', 'Professional')], max_length=20, null=True)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('height', models.FloatField(blank=True, help_text='cm', null=True)),
                ('weight', models.FloatField(blank=True, help_text='kg', null=True)),
                ('measurements_bicep', models.PositiveIntegerField(blank=True, help_text='cm', null=True)),
                ('measurements_forearm', models.PositiveIntegerField(blank=True, help_text='cm', null=True)),
                ('measurements_shoulder', models.PositiveIntegerField(blank=True, help_text='cm', null=True)),
                ('measurements_chest', models.PositiveIntegerField(blank=True, help_text='cm', null=True)),
                ('measurements_waist', models.PositiveIntegerField(blank=True, help_text='cm', null=True)),
                ('measurements_hips', models.PositiveIntegerField(blank=True, help_text='cm', null=True)),
                ('measurements_calves', models.PositiveIntegerField(blank=True, help_text='cm', null=True)),
                ('next_workout_type', models.CharField(choices=[('push', 'Push'), ('pull', 'Pull'), ('legs', 'Legs')], default='push', max_length=10)),
                ('subscription_type', models.CharField(blank=True, choices=[('1_month', '1 Month'), ('3_months', '3 Months'), ('6_months', '6 Months')], max_length=20, null=True)),
                ('subscription_start', models.DateField(blank=True, null=True)),
                ('subscription_end', models.DateField(blank=True, null=True)),
                ('role', models.CharField(choices=[('member', 'Member'), ('coach', 'Coach'), ('employee', 'Employee')], default='member', max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('goal', models.ManyToManyField(blank=True, related_name='users', to='users.goal')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
