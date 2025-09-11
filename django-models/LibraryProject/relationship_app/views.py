from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy

# from .forms import UserRegistrationForm

# Function-based View to list all books
def list_books(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', 'Book.objects.all()')

# Class-based View to display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'



# Create a custom view for user registration.
def register_view(request):
    """
    Handles user registration.
    If the request is a POST, it attempts to validate the form and create a new user.
    If the request is a GET, it displays the registration form.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after successful registration
            login(request, user)
            return redirect('login') # Redirect to the login page
    else:
        form = UserCreationForm()
    
    return render(request, 'relationship_app/register.html', {'form': form})

# Use Django's built-in LoginView and LogoutView for simplicity and security.
# They handle the form validation and session management automatically.
class UserLoginView(LoginView):
    """
    Handles user login using Django's built-in view.
    It uses the specified template and redirects to the 'home' page on success.
    """
    template_name = 'relationship_app/login.html'
    
class UserLogoutView(LogoutView):
    """
    Handles user logout using Django's built-in view.
    It uses the specified template and redirects to the 'login' page on logout.
    """
    next_page = reverse_lazy('login')
