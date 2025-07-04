from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.activities.views import *

router = DefaultRouter()
router.register(r'registration', ExtraActivityRegistrationViewSet, basename='registration')
router.register(r'', ExtraActivityViewSet, basename='activities')

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += router.urls