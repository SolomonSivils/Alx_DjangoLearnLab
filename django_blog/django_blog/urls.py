from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include all built-in auth URLs (login, logout, password reset, etc.)
    path('', include('django.contrib.auth.urls')), 
    # Include the URLs from the 'blog' app for registration and profile
    path('', include('blog.urls')),
]