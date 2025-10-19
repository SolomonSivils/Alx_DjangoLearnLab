# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Additional fields
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Followers field (Many-to-Many relationship with itself)
    # symmetrical=False is necessary because following is not always mutual.
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following', # Reverse relationship name: a user's 'following'
        blank=True
    )

    def __str__(self):
        return self.username