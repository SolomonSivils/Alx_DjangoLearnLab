from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    class Meta:
        permissions = [
            ("can_add_book", "Can add a book"),
            ("can_change_book", "Can change a book"),
            ("can_delete_book", "Can delete a book"),
        ]

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library,  on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
# Define the choices for the user's role
ROLE_CHOICES = (
    ('Admin', 'Admin'),
    ('Librarian', 'Librarian'),
    ('Member', 'Member'),
)

class UserProfile(models.Model):
    """
    Extends the built-in Django User model to include a role field.
    This model has a one-to-one relationship with the User model.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userprofile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return self.user.username

# Django Signal to automatically create a UserProfile
# whenever a new User object is created.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Listens for the 'post_save' signal from the User model.
    If a new User is created, it also creates an associated UserProfile.
    """
    if created:
        UserProfile.objects.create(user=instance)

# Django Signal to save the UserProfile whenever the User is saved.
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Ensures that when a User object is updated, its associated
    UserProfile is also saved.
    """
    instance.userprofile.save()
