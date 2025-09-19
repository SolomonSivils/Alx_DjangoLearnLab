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
    
    # URL pattern for user login using Django's built-in LoginView
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),

    # URL pattern for user logout using Django's built-in LogoutView
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('librarian_view/', views.librarian_view, name='librarian_view'),
    path('member_view/', views.member_view, name='member_view'),
    path('add_book/', views.add_book_view, name='add_book'),
    path('edit_book/<int:book_id>/', views.edit_book_view, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book_view, name='delete_book'),
]


