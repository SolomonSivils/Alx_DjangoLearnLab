from django.shortcuts import render
# accounts/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserRegistrationSerializer, CustomUserSerializer
from .models import CustomUser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.views import APIView

User = get_user_model() # Get your CustomUser model

# New View to Follow a User
class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    # No serializer_class or queryset is needed for this simple action

    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user == user_to_follow:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(user_to_follow)
        
        return Response(
            {"status": f"You are now following {user_to_follow.username}"}, 
            status=status.HTTP_200_OK
        )

# New View to Unfollow a User
class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    # No serializer_class or queryset is needed for this simple action

    def post(self, request, user_id):
        try:
            user_to_unfollow = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        request.user.following.remove(user_to_unfollow)

        return Response(
            {"status": f"You have unfollowed {user_to_unfollow.username}"}, 
            status=status.HTTP_200_OK
        )

# Registration View
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Automatically create and return a token upon successful registration
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "user": serializer.data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)


# Custom Login View (to return user data with the token)
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

# Profile View (Retrieve/Update logged-in user's profile)
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated] # Requires a valid token

    def get_object(self):
        # Return the profile of the currently logged-in user
        return self.request.user
    


# ... (Existing views like RegisterView, etc.)

request.user.following.add(user_to_follow)

# 🔗 ADD NOTIFICATION HOOK: Notify the followed user
create_notification(
    recipient=user_to_follow,
    actor=request.user,
    verb="started following you"
)

return Response(
    {"status": f"You are now following {user_to_follow.username}"}, 
    status=status.HTTP_200_OK
)
