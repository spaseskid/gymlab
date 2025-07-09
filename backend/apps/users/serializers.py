from rest_framework import serializers
from apps.users.models import User, Goal


class UserSerializer(serializers.ModelSerializer):
    goal = serializers.PrimaryKeyRelatedField(many=True, queryset=Goal.objects.all())

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'name', 'surname', 'phone_number', 'member_id', 'image',
            'gender', 'program_level', 'age', 'height', 'weight', 'goal',
            'measurements_bicep', 'measurements_forearm', 'measurements_shoulder', 'measurements_chest',
            'measurements_waist', 'measurements_hips', 'measurements_calves',
            'next_workout_type', 'subscription_type', 'subscription_start',
            'subscription_end', 'role'
        ]
        read_only_fields = ['member_id', 'subscription_start', 'subscription_end', 'subscription_type']



