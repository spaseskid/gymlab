# Generated by Django 5.2.3 on 2025-07-01 22:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('activities', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='extraactivity',
            name='coach',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 'coach'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='extraactivityregistration',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='activities.extraactivity'),
        ),
        migrations.AddField(
            model_name='extraactivityregistration',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='extraactivityregistration',
            unique_together={('user', 'activity')},
        ),
    ]
