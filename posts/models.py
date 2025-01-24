from django.core.validators import RegexValidator
from django.db import models


class User(models.Model):
    username = models.CharField(
        max_length=50,
        validators=[RegexValidator(regex='^[a-zA-Z0-9]*$', message='Username must be alphanumeric', code="invalid_username")] #add validation here, username should be alphanumeric
    )
    email = models.EmailField(unique=True) # EmailField is a built-in email validator
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.username


class Post(models.Model):
    content = models.TextField() # The main content of the post
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE) # Links the post to its author
    created_at = models.DateTimeField(auto_now_add=True) # Timestamp for when the post is created


    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"


class Comment(models.Model):
    text = models.TextField(blank=False) # The main content of the comment
                                         # add a field level validation, blank field will not be accepted
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE) # Links the comment to its author
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE) # Links the comment to a specific post
    created_at = models.DateTimeField(auto_now_add=True) # Timestamp for when the comment is created


    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.id}"
