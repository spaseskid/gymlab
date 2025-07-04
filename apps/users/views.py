from rest_framework.exceptions import PermissionDenied
from django.shortcuts import render
from rest_framework import viewsets, permissions, mixins
from apps.users.models import User, Goal
from apps.users.serializers import UserSerializer, GoalSerializer

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
            serializer.save(id=user.id)

class GoalViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]
