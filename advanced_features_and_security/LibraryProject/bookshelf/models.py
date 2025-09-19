from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"
    
class CustomUser(AbstractUser):
    # Your custom fields
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    # REQUIRED_FIELDS must be a list of field names
    # Add any custom fields you want to be required here
    REQUIRED_FIELDS = ['date_of_birth'] 
    
    def __str__(self):
        return self.username
    
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    class Meta:
        permissions = [
            ('can_view'),
            ('can_create'),
            ('can_edit'),
            ('can_delete'),
        ]
    def __str__(self):
        return self.title

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

    
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    class Meta:
        permissions = [
            ("can_view", "Can view all posts"),
            ("can_create", "Can create a new post"),
            ("can_edit", "Can edit a post"),
            ("can_delete", "Can delete a post"),
        ]

    def __str__(self):
        return self.title
    
# blog/models.py



class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ('can_view', 'Can view article'),
            ('can_create', 'Can create article'),
            ('can_edit', 'Can edit article'),
            ('can_delete', 'Can delete article'),
        ]
    def __str__(self):
        return self.title
    
