from rest_framework import serializers
from backend.apps.workouts.models import *

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'
        read_only_fields = ('id', 'category', 'name', 'youtube_link', 'description',
                            'order', 'is_active', 'created_at', 'reps', 'duration', 'program_level')

class WorkoutSessionSerializer(serializers.ModelSerializer):
    exercises_completed = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutSession
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'is_active', 'user', 'completed_date','duration', 'workout_type')