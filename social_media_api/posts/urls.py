# posts/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, CommentViewSet, FeedView, LikePostView, UnlikePostView

router = DefaultRouter()
# Register the Post routes: /posts/, /posts/{pk}/
router.register(r'posts', PostViewSet)
# Register the Comment routes: /comments/, /comments/{pk}/
router.register(r'comments', CommentViewSet)

urlpatterns = [
    # Include all routes defined by the router
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='user-feed'), # 🔗 ADD THIS LINE
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
]