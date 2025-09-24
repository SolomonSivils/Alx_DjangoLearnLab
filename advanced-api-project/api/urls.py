"""
This module defines the URL patterns for the API application.
"""
from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView, AuthorListCreateView

# Define URL patterns for the API endpoints
urlpatterns = [
    # Paths for the Book model
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),

    # Path for the Author model
    path('authors/', AuthorListCreateView.as_view(), name='author-list-create'),
]
