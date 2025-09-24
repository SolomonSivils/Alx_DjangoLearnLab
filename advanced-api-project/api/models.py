"""
This module defines the data models for the API.
"""
from django.db import models

class Author(models.Model):
    """
    Represents an author of books.
    
    A one-to-many relationship is established where one author can have
    multiple books.
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Represents a book.
    
    This model has a foreign key to the Author model, linking each book
    to its respective author. The `related_name` argument is crucial here.
    It allows us to access all the books associated with an author
    from the Author instance itself (e.g., `author.books.all()`).
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author, 
        related_name='books', 
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return f"{self.title} ({self.publication_year})"