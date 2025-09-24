from django.shortcuts import render
"""
This module defines the views for the API using Django REST Framework's
generic views and mixins.
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
from django_filters import rest_framework
from .serializers import BookSerializer, AuthorSerializer
from .models import Book, Author

# Individual Generic Views for the Book model

class BookListView(generics.ListAPIView):
    """
    A view for listing all books.
    This view provides a list of all Book instances.
    It supports filtering, searching, and ordering.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Define the filter backends to use
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Fields to allow filtering on
    filterset_fields = ['title', 'author', 'publication_year']
    
    # Fields to allow searching on (case-insensitive)
    search_fields = ['title', 'author__name']
    
    # Fields to allow ordering on
    ordering_fields = ['title', 'publication_year']

class BookDetailView(generics.RetrieveAPIView):
    """
    A view for retrieving a single book instance by its ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookCreateView(generics.CreateAPIView):
    """
    A view for creating a new book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookUpdateView(generics.UpdateAPIView):
    """
    A view for updating an existing book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    """
    A view for deleting an existing book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# Generic View for the Author model
class AuthorListCreateView(generics.ListCreateAPIView):
    """
    A view for listing all authors and creating a new author.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
