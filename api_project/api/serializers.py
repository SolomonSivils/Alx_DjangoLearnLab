from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """
    A serializer for the Book model.
    Serializers convert complex data types, like our Book model instances,
    into native Python data types that can be easily rendered into JSON, XML, etc.
    """
    class Meta:
        # The model to be serialized
        model = Book
        # The fields from the model to be included in the serialized output
        fields = '__all__'