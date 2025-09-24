from django.shortcuts import render
"""
This module defines the views for the API using Django REST Framework's
generic views and mixins.
"""
from rest_framework import generics
from rest_framework import permissions
from .serializers import BookSerializer
from .models import Book

# Generic Views for the Book model

class BookListView(generics.ListCreateAPIView):
    """
    A view for listing all books and creating a new book.

    This view combines the functionality of generics.ListAPIView and
    generics.CreateAPIView using the ListCreateAPIView class.
    It lists all available Book instances and allows for the creation of a new
    Book instance.

    Permissions: Read-only access is allowed for anyone.
    To create a new book, the user must be authenticated.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Apply permissions: read-only access for anyone, but only authenticated users can create.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    A view for retrieving, updating, and deleting a single book instance.

    This view combines the functionality of generics.RetrieveAPIView,
    generics.UpdateAPIView, and generics.DestroyAPIView. It fetches a single
    Book instance by its primary key (pk) and allows for its retrieval,
    modification, or deletion.

    Permissions: Read-only access is allowed for anyone.
    To update or delete a book, the user must be authenticated.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Apply permissions: read-only access for anyone, but only authenticated users can update or delete.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
