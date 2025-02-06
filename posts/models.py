from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models



class User(AbstractUser):
    username = models.CharField(
        max_length=50,
        unique=True)
    email = models.EmailField(unique=True) # EmailField is a built-in email validator
    password = models.CharField( max_length=50, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.username


class Post(models.Model):
    POST_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=200)  # Add a title for the post
    content = models.TextField(blank=False)   # The main content of the post
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)  # Link the post to its author
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default='General')  # Type of the post (e.g., text, image, video)
    metadata = models.JSONField(default=dict, blank=True)  # Store additional metadata (e.g., file_size, duration)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the post is created

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"


class Comment(models.Model):
    text = models.TextField(blank=False)  # Ensures comment text cannot be blank
    author = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE
    )  # Links comment to the author
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE
    )  # Links comment to a specific post
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for comment creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for last update

    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.id}"

