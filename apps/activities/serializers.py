from rest_framework import serializers
from apps.activities.models import *
from apps.users.serializers import UserSerializer


class ExtraActivitySerializer(serializers.ModelSerializer):
    coach = UserSerializer(read_only=True)

    class Meta:
        model = ExtraActivity
        fields = [
            'id', 'title', 'description', 'start_time', 'duration', 'capacity',
            'coach', 'day_of_week', 'program_level'
        ]


class ExtraActivityRegistrationSerializer(serializers.ModelSerializer):
    activity = ExtraActivitySerializer(read_only=True)
    activity_id = serializers.PrimaryKeyRelatedField(
        queryset=ExtraActivity.objects.all(), source='activity', write_only=True
    )
    class Meta:
        model = ExtraActivityRegistration
        fields = ['id', 'user', 'activity', 'activity_id', 'registered_at', 'waiting']
        read_only_fields = ['registered_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)