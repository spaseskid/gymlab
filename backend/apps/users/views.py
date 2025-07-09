from datetime import timedelta
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import render
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.workouts.models import WorkoutSession

from apps.users.models import User, Goal
from apps.users.serializers import UserSerializer
from apps.workouts.serializers import WorkoutSessionSerializer


# Create your views here.

class IsCurrentOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser or request.user.role in ['coach', 'employee']:
            return True
        return obj == request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsCurrentOrStaff]

    def get_queryset(self):
        user = self.request.user
        # Coaches, employees, superusers see all users
        if user.is_staff or user.is_superuser or user.role in ['coach', 'employee']:
            return User.objects.all()
        # Regular users see only themselves
        return User.objects.filter(id=user.id)

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied("User deletion is not allowed via API")

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff or user.is_superuser or user.role in ['coach', 'employee']:
            return super().create(request, *args, **kwargs)
        else:
            raise PermissionDenied("Only staff can create users, so visit the Gym")

    def perform_update(self, serializer):
        user = self.request.user
        # Staff, superusers, coaches, employees can update any user
        if user.is_staff or user.is_superuser or user.role in ['coach', 'employee']:
            serializer.save()
        else:
            # Normal user can update only their own data
            if serializer.instance != user:
                raise PermissionDenied("You can only update your own data.")
            serializer.save()



class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # Recent workouts (last 5)
        recent_workouts = WorkoutSession.objects.filter(user=user).order_by('-completed_date')[:5]
        recent_workouts_serialized = WorkoutSessionSerializer(recent_workouts, many=True).data

        # Workout calendar dates (completed)
        all_dates = WorkoutSession.objects.filter(user=user).values_list('completed_date', flat=True)
        calendar_dates = [dt.date() for dt in all_dates]

        # Basic info + measurements + subscription status
        data = {
            'id': user.id,
            'name': user.name,
            'surname': user.surname,
            'member_id': user.member_id,
            'image': user.image.url if user.image else None,
            'program_level': user.program_level,
            'gender': user.gender,
            'age': user.age,
            'height': user.height,
            'weight': user.weight,
            'next_workout_type': user.get_next_workout_type_display(),
            'has_active_subscription': user.has_active_subscription(),
            'days_remaining': user.days_remaining(),
            'measurements': {
                'bicep': user.measurements_bicep,
                'forearm': user.measurements_forearm,
                'shoulder': user.measurements_shoulder,
                'chest': user.measurements_chest,
                'waist': user.measurements_waist,
                'hips': user.measurements_hips,
                'calves': user.measurements_calves,
            },
            'recent_workouts': recent_workouts_serialized,
            'workout_dates': calendar_dates,
        }
        return Response(data)
