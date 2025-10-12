from django.urls import path
from . import views
# Import the CBVs directly for cleaner mapping
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)

urlpatterns = [
    # READ: List all posts (Home page)
    path('', PostListView.as_view(), name='post-list'),

    # READ: Detail view for a single post
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    
    # CREATE: New post
    path('post/new/', PostCreateView.as_view(), name='post-create'),

    # UPDATE: Edit an existing post
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),

    # DELETE: Delete an existing post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    
    # Include existing authentication URLs (if you kept them in blog/urls.py)
    # If not, ensure they are still included in django_blog/urls.py
    path('register/', views.register_user, name='register'),
    path('profile/', views.user_profile, name='profile'),
]