from django.urls import path
from .views import LibraryDetailView
from .views import list_books

urlpatterns = [
    # URL for the function-based view
    path('books/', list_books, name='book-list'),
    
    # URL for the class-based view. The <int:pk> captures the primary key.
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]