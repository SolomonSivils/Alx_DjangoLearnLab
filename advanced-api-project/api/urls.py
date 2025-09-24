"""
This module defines the URL patterns for the API application.
"""
from django.urls import path
from .views import BookListView, BookDetailView

# Define URL patterns for the API endpoints
urlpatterns = [
    # Path for listing all books and creating a new book.
    # The .as_view() method is used to convert the class-based view into a callable function.
    path('books/', BookListView.as_view(), name='book-list-create'),

    # Path for retrieving, updating, or deleting a single book by its primary key (pk).
    # The <int:pk> part is a dynamic URL parameter that captures the book's ID.
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
]
