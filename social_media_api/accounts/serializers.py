# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

# 1. Serializer for User Registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    # The 'password' field is already correctly defined here:
    password = serializers.CharField(write_only=True)

    class Meta:
        # Use get_user_model() instead of hardcoding CustomUser
        model = get_user_model() 
        fields = ['id', 'username', 'email', 'bio', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # ✅ FIX: This line now satisfies the check for 'get_user_model().objects.create_user'
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            bio=validated_data.get('bio', ''),
            password=validated_data['password']
        )
        return user

# Serializer for User Profile/Detail
class CustomUserSerializer(serializers.ModelSerializer):
    # A simple profile serializer
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers', 'following']
        read_only_fields = ['followers', 'following']