"""
URL configuration for social_media_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# social_media_api/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # API endpoints will be prefixed with 'api/'
    path('api/accounts/', include('accounts.urls')),
    # You could also add a root path for API
    # path('api/', include('accounts.urls')),
    # Link the accounts app for auth routes
    path('api/auth/', include('accounts.urls')), 
    
    # 🔗 ADD THIS LINE to include post and comment routes
    path('api/', include('posts.urls')),
    path('api/notifications/', include('notifications.urls')),
]