from django.urls import path
from . import views

urlpatterns = [
    # Custom registration view
    path('register/', views.register_user, name='register'),
    
    # Custom profile view
    path('profile/', views.user_profile, name='profile'),
    
    # You can also customize the built-in paths if needed, 
    # but for this task, the django.contrib.auth.urls handle 'login/' and 'logout/'
    
    # Example: If you wanted a custom logout view:
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
]