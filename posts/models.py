from django.db import models

# Create your models here.
class User(models.Model):
            username = models.CharField(max_length=100, unique=True)  # User's unique username
            email = models.EmailField(unique=True)
            created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the user was created


            def __str__(self):
                return self.username
            
class Post(models.Model):
            content = models.TextField()  # The text content of the post
            author = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who created the post
            created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the post was created


            def __str__(self):
                return self.content[:50]
            


