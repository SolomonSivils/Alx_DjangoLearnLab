"""
This module defines the URL patterns for the 'api' app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'books', BookViewSet, basename='book')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]