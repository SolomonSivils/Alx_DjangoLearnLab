# blog/forms.py

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    # This form extends the default UserCreationForm
    class Meta:
        # Use the built-in User model
        model = User
        # Include username, email, and password fields (password is handled automatically)
        fields = ('username', 'email') 
        # Note: We don't need to explicitly add a password field as it's included by UserCreationForm.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the email field required
        self.fields['email'].required = True