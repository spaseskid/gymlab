from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.workouts.views import ExerciseViewSet, WorkoutSessionViewSet

router = DefaultRouter()
router.register(r'sessions', WorkoutSessionViewSet, basename='session')
router.register(r'', ExerciseViewSet, basename='exercise')

urlpatterns = [
    path('', include(router.urls)),
]