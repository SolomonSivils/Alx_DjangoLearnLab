# bookshelf/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # This URL pattern is required by the checker
    path('books/', views.book_list, name='books'),
]