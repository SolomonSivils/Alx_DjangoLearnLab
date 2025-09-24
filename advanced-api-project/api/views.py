from django.shortcuts import render
"""
This module defines the views for the API using Django REST Framework's
generic views and mixins.
"""
from rest_framework import generics
from rest_framework import permissions
from .serializers import BookSerializer, AuthorSerializer
from .models import Book, Author

# Individual Generic Views for the Book model

class BookListView(generics.ListAPIView):
    """
    A view for listing all books.
    This view provides a list of all Book instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookDetailView(generics.RetrieveAPIView):
    """
    A view for retrieving a single book instance by its ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookCreateView(generics.CreateAPIView):
    """
    A view for creating a new book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookUpdateView(generics.UpdateAPIView):
    """
    A view for updating an existing book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    """
    A view for deleting an existing book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

# Generic View for the Author model
class AuthorListCreateView(generics.ListCreateAPIView):
    """
    A view for listing all authors and creating a new author.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
