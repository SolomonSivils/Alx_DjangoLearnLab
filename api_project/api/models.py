from django.db import models

# Create your models here.

class Book(models.Model):
    """
    A simple model to represent a book with a title and an author.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)

    def __str__(self):
        """
        String representation of the Book model.
        This is useful for displaying in the Django admin.
        """
        return self.title