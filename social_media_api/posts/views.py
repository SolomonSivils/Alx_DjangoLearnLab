from django.shortcuts import render
# posts/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly # Import your custom permission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters # 💡 Import DRF filters

class PostViewSet(viewsets.ModelViewSet):
    # Retrieve all posts
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    # Apply IsAuthenticated for list/create, and IsAuthorOrReadOnly for update/delete
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    # 💡 Add Filtering and Searching capabilities
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'content'] # Fields to search against
    # You can also add filterset_fields = ['author__username'] for exact filtering

    # Automatically set the author when a post is created
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    # Retrieve all comments
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    # Automatically set the author when a comment is created
    def perform_create(self, serializer):
        # NOTE: The post field must be passed in the request data
        serializer.save(author=self.request.user)