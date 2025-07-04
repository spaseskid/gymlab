from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users.views import UserViewSet, GoalViewSet

router = DefaultRouter()
router.register(r'goals', GoalViewSet, basename='goal')
router.register(r'', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
]