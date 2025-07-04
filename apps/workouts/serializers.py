from rest_framework import serializers
from apps.workouts.models import *

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'
        read_only_fields = ('id', 'created_at')

class WorkoutSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSession
        fields = '__all__'