from django.urls import path
from .views import book_list, LibraryDetailView

urlpatterns = [
    # URL for the function-based view
    path('books/', book_list, name='book-list'),
    
    # URL for the class-based view. The <int:pk> captures the primary key.
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]