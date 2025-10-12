from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm # For profile editing

# -----------------------------------------------------------------
# 1. Registration View
# -----------------------------------------------------------------
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log the user in after registration
            login(request, user) 
            messages.success(request, "Registration successful! Welcome to the blog.")
            return redirect('profile') # Redirect to the profile page
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'blog/register.html', {'form': form})

# -----------------------------------------------------------------
# 2. Profile View (View/Edit)
# -----------------------------------------------------------------
# The @login_required decorator ensures only logged-in users can access this page
@login_required
def user_profile(request):
    # We use Django's default UserChangeForm for simplicity in this step.
    # A custom profile form would be better in a real app.
    if request.method == 'POST':
        # Pass instance=request.user so the form is pre-filled and updates the existing user
        form = UserChangeForm(request.POST, instance=request.user) 
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was updated successfully!")
            # Note: UserChangeForm includes sensitive fields. 
            # In a real app, you would use a form that excludes 'password'.
            return redirect('profile')
        else:
            messages.error(request, "Error updating profile.")
    else:
        form = UserChangeForm(instance=request.user)

    # Exclude password fields for security and better UX in the template
    form.fields.pop('password', None)
    
    return render(request, 'blog/profile.html', {'form': form})