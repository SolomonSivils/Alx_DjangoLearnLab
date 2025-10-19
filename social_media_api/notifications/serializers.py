# notifications/serializers.py

from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    # Display the username of the user who performed the action
    actor_username = serializers.ReadOnlyField(source='actor.username') 
    
    # Optional: Display the target object's primary key and type
    target_object_id = serializers.ReadOnlyField(source='object_id')
    target_content_type = serializers.ReadOnlyField(source='content_type.model')

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'actor', 'actor_username', 'verb', 
            'target_content_type', 'target_object_id', 
            'timestamp', 'is_read'
        ]
        read_only_fields = fields # Notifications are only viewed, not created via API