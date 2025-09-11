from django.urls import path
from .views import LibraryDetailView
from .views import list_books
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # URL for the function-based view
    path('books/', list_books, name='book-list'),
    
    # URL for the class-based view. The <int:pk> captures the primary key.
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    # URL pattern for user registration, linking to our custom view
    path('register/', views.register_view, name='register'),
    
    # URL pattern for user login, using Django's built-in LoginView
    path('login/', views.UserLoginView.as_view(), name='login'),

    # URL pattern for user logout, using Django's built-in LogoutView
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]


