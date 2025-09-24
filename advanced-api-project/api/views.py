from django.shortcuts import render
"""
This module defines the views for the API using Django REST Framework.
"""
from rest_framework import viewsets
from .serializers import AuthorSerializer, BookSerializer
from .models import Author, Book

class AuthorViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Author instances.
    
    This view uses the AuthorSerializer to handle serialization and
    deserialization of Author objects.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Book instances.
    
    This view uses the BookSerializer to handle serialization and
    deserialization of Book objects.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer