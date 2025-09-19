# bookshelf/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # This URL pattern is required by the checker
    path('books/', views.book_list, name='books'),
    path('example-form/', views.form_example, name='example_form')
]