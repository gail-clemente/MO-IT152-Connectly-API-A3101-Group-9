from rest_framework import serializers
from .models import User, Post, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        error_messages={'does_not_exist': 'Author not found.'}
    )
    
    comments = serializers.StringRelatedField(many=True, read_only=True)


    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at', 'comments']
       


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
        fields = ['id', 'text', 'author', 'post', 'created_at']


    def validate_post(self, value):
        if not Post.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Post not found.")
        return value


    def validate_author(self, value):
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Author not found.")
        return value
