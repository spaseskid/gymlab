from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.apps.users.views import UserViewSet, DashboardView

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')


urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', include(router.urls)),
]