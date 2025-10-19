from django.shortcuts import render
# posts/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly # Import your custom permission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters # 💡 Import DRF filters
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from notifications.utils import create_notification # 💡 Import the helper

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
        comment = serializer.save(author=self.request.user)
        post_author = comment.post.author
        
        # 🔗 ADD NOTIFICATION HOOK: Notify the post author
        if comment.author != post_author:
            create_notification(
                recipient=post_author, 
                actor=comment.author, 
                verb="commented on your post", 
                target=comment.post
            )

class FeedView(generics.ListAPIView):
    # This view only allows listing (GET) posts.
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 1. Get the list of users that the current request user is following.
        # This returns a queryset of CustomUser objects.
        followed_users = self.request.user.following.all()

        # 2. Filter all Posts to include only those whose author is in the followed_users list.
        # The 'author__in' lookup is used here.
        queryset =Post.objects.filter(author__in=following_users).order_by('-created_at')

        # 3. Order the posts by created_at, showing the newest first.
        return queryset

# NOTE: Since you implemented pagination in the last task, 
# this view will automatically be paginated!

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        # 1. Check if already liked
        if Like.objects.filter(user=user, post=post).exists():
            return Response({"detail": "Post already liked."}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Create the Like object
        Like.objects.create(user=user, post=post)

        # 3. Create a Notification for the post author (if not self-liking)
        if user != post.author:
            create_notification(
                recipient=post.author, 
                actor=user, 
                verb="liked your post", 
                target=post
            )

        return Response({"status": "Post liked successfully."}, status=status.HTTP_201_CREATED)

class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        # 1. Find the Like object
        like_qs = Like.objects.filter(user=user, post=post)

        if not like_qs.exists():
            return Response({"detail": "Post is not liked by this user."}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Delete the Like object
        like_qs.delete()
        
        # NOTE: We don't typically delete the "like" notification upon unlike

        return Response({"status": "Post unliked successfully."}, status=status.HTTP_200_OK)