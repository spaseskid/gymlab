from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from apps.workouts.models import *
from apps.workouts.serializers import *
# Create your views here.

class IsCurrentOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or request.user.is_superuser or request.user.role in ['coach','employee']


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsCurrentOrStaff]

class WorkoutSessionViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role in ['coach','employee']:
            return WorkoutSession.objects.all()
        return WorkoutSession.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role in ['coach','employee']:
            serializer.save()
        else:
            raise PermissionDenied('You do not have permission to perform this action')




