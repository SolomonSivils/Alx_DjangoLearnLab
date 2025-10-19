# notifications/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import NotificationViewSet

router = DefaultRouter()
# /notifications/ and /notifications/{pk}/
router.register(r'', NotificationViewSet, basename='notification')

urlpatterns = [
    # Include all routes defined by the router (e.g., /notifications/, /notifications/mark_all_as_read/)
    path('', include(router.urls)),
]