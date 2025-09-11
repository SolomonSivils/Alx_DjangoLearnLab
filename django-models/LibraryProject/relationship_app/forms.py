from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    """
    Custom form for user registration.
    It inherits from Django's built-in UserCreationForm to handle password hashing
    and validation automatically.
    """
    class Meta:
        model = User
        fields = ["username", "email"]