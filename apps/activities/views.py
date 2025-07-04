from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from apps.activities.models import ExtraActivity, ExtraActivityRegistration
from apps.activities.serializers import ExtraActivitySerializer, ExtraActivityRegistrationSerializer


# Create your views here.

class IsStaffOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # Write permissions only for staff roles
        return request.user and (
                request.user.is_staff or
                request.user.is_superuser or
                request.user.role in ['coach', 'employee']
        )

class ExtraActivityViewSet(viewsets.ModelViewSet):
    queryset = ExtraActivity.objects.all()
    serializer_class = ExtraActivitySerializer
    permission_classes = [IsStaffOrReadOnly]


class ExtraActivityRegistrationViewSet(viewsets.ModelViewSet):
    queryset = ExtraActivityRegistration.objects.all()
    serializer_class = ExtraActivityRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role in ['coach', 'employee']:
            return ExtraActivityRegistration.objects.all()
        return ExtraActivityRegistration.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role in ['coach', 'employee'] or serializer.instance.user == user:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update this registration")

    def perform_destroy(self, instance):
        if not self.request.user.is_staff and instance.user != self.request.user:
            raise PermissionDenied("Do you really want to UNREGISTER from the Activity?")
        instance.delete()