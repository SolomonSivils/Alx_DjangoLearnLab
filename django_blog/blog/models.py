from django.db import models
from django.contrib.auth.models import User # Import the built-in User model

class Post(models.Model):
    # Field 1: Title of the blog post
    title = models.CharField(max_length=200)
    
    # Field 2: Content/Body of the blog post
    content = models.TextField()
    
    # Field 3: Date/Time the post was published (set automatically on creation)
    published_date = models.DateTimeField(auto_now_add=True)
    
    # Field 4: Author of the post (Foreign Key to Django's User model)
    # on_delete=models.CASCADE means if the User is deleted, their posts are also deleted.
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    # Optional: A human-readable representation of the object
    def __str__(self):
        return self.title