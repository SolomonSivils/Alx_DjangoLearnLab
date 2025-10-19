from django.shortcuts import render
# notifications/views.py

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

# Use ListModelMixin to list, RetrieveModelMixin to view single, 
# and UpdateModelMixin to mark as read
class NotificationViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only show notifications where the current user is the recipient
        return Notification.objects.filter(recipient=self.request.user)

    # Custom action to mark all unread notifications as read
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        queryset = self.get_queryset().filter(is_read=False)
        count = queryset.update(is_read=True)
        return Response({'status': f'{count} notifications marked as read.'})