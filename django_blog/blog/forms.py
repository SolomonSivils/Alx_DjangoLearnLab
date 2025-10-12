# blog/forms.py

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Post,  Comment # Import Comment model
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

class CommentForm(forms.ModelForm):
    # Customize the widget to make the textarea friendlier
    content = forms.CharField(widget=forms.Textarea(attrs={
        'rows': '3', 
        'placeholder': 'Join the discussion...'
    }), label='')
    
    class Meta:
        model = Comment
        # Only expose the content field to the user. 
        # 'post', 'author', and 'created_at' will be set in the view.
        fields = ['content'] 