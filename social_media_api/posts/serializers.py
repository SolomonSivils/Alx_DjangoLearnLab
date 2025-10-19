# posts/serializers.py

from rest_framework import serializers
from .models import Post, Comment

# Helper Serializer for nested Comment details (will be used in PostSerializer)
class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'content', 'created_at']
        read_only_fields = ['author', 'post']

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    # Use a nested serializer to show comments when retrieving a single post
    comments = CommentSerializer(many=True, read_only=True) 

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'title', 'content', 'created_at', 'updated_at', 'comments']
        read_only_fields = ['author'] # Prevent accidental modification of author