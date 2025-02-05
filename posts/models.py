from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models



class User(AbstractUser):
    username = models.CharField(
        max_length=50,
        unique=True)
    email = models.EmailField(unique=True) # EmailField is a built-in email validator
    password = models.CharField( max_length=50, blank=False,
        validators=[RegexValidator(regex='^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$', message="Password should contain the following: lowercase and uppercase letter, number and should be more than 8 characters long. ",
                                     code="invalid_password")])
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.username


class Post(models.Model):
    content = models.TextField(blank=False) # The main content of the post
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE) # Links the post to its author
    created_at = models.DateTimeField(auto_now_add=True) # Timestamp for when the post is created


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

