# blog/forms.py

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Post
# We will keep the CustomUserCreationForm from the previous step


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

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # The author field is set automatically in the PostCreateView's form_valid method, 
        # so we only include title and content here.
        fields = ['title', 'content'] 
        widgets = {
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }