# notifications/utils.py

from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(recipient, actor, verb, target=None):
    """
    Helper function to quickly create and save a Notification instance.
    """
    if target:
        content_type = ContentType.objects.get_for_model(target)
        object_id = target.pk
    else:
        content_type = None
        object_id = None
        
    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        content_type=content_type,
        object_id=object_id
    )