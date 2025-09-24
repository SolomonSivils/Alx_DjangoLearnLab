"""
This module defines the serializers for the API models.
"""
from rest_framework import serializers
from .models import Author, Book
from datetime import date

class BookSerializer(serializers.ModelSerializer):
    """
    Serializes all fields for the Book model.
    
    This serializer also includes custom validation to ensure that a book
    is not published in the future.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        
    def validate_publication_year(self, value):
        """
        Custom validation to check that the publication year is not in the future.
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. The current year is {current_year}."
            )
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes the Author model, including its related books as a nested object.
    
    The 'books' field uses the BookSerializer to represent the one-to-many
    relationship dynamically. The `many=True` and `read_only=True` arguments
    are crucial here. `many=True` tells the serializer to expect a list of books,
    and `read_only=True` ensures that this field is used for representation only
    and is not required for creating or updating an Author instance.
    """
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
