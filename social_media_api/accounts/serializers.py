# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser

# Serializer for User Registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        # Exclude profile_picture and followers for registration
        fields = ['id', 'username', 'email', 'bio', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Use Django's built-in method to correctly hash the password
        user = CustomUser.objects.create_user(
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