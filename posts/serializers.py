from django.forms import ValidationError
from rest_framework import serializers
from rest_framework import status
from .models import Post, Comment
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from django.core.validators import RegexValidator

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,  # Password is used only for writing
        required=True,  # Ensure that password is required
        validators=[RegexValidator(
            regex='^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$',
            message="Password should contain the following: lowercase and uppercase letter, number, and should be more than 8 characters long.",
            code="invalid_password")]
    )
    
    class Meta:
        model = User
        fields = ['id','username', 'email', 'password', 'created_at']  # Include password for creation only

    def create(self, validated_data):
        password = validated_data.pop('password')  # Remove the password from validated data
        user = User.objects.create(**validated_data)
        user.set_password(password)  # Use Django's built-in password hashing
        user.save()
        return user


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        error_messages={'does_not_exist': 'Author not found.'}
    )
    comments = serializers.StringRelatedField(many=True, read_only=True)


    class Meta:
        model = Post
        fields = [ 'content', 'author', 'created_at', 'comments']


    def validate_author(self, value):
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Author not found.")
        return value
       

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),
        error_messages={'does_not_exist': 'Post not found.'}
    )
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        error_messages={'does_not_exist': 'Author not found.'}
    )

    class Meta:
        model = Comment
        fields = [ 'text', 'author', 'post', 'created_at']


    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment text cannot be empty.")
        return value
    
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
            raise PermissionDenied("Authentication is required.")


