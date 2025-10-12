# blog/models.py

from django.db import models
from django.contrib.auth.models import User # Ensure this is imported
from taggit.managers import TaggableManager # Import TaggableManager
# from .models import Post (already defined above)


# ... (Post model definition is here) ...

class Comment(models.Model):
    # Foreign Key to the Post it belongs to (many comments to one post)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    
    # Foreign Key to the User who wrote the comment
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # The actual content of the comment
    content = models.TextField()
    
    # Timestamp for creation (set automatically on object creation)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Timestamp for last update (set automatically every time the object is saved)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Order comments by the oldest first (or newest, depending on preference)
        ordering = ['created_at'] 

    def __str__(self):
        # Display the comment's author and content snippet in the admin
        return f'{self.author.username}: {self.content[:30]}...'
    
class Post(models.Model):
    # ... (Existing fields: title, content, published_date, author) ...
    
    # NEW FIELD: Tags field using TaggableManager
    tags = TaggableManager() # Adds a tags field to the Post model

    # ... (Existing __str__ and get_absolute_url methods) ...
    
# ... (Comment model remains the same) ...