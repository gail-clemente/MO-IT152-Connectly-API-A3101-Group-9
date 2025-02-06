from argon2 import hash_password
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from connectly_project.singletons.logger_singleton import LoggerSingleton
from .models import Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from posts import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
import bcrypt
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin, IsCommentAuthor, IsPostAuthor, IsOwner
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .permissions import IsAdmin 
from .factories.post_factory import PostFactory

User = get_user_model()
logger = LoggerSingleton().get_logger()


class ProtectedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        return Response({"message": "Authenticated!"})


class UserListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]  # Only admins can view all users, but any authenticated user can register

    def get(self, request):
        """Only admin users can view all users."""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Handles password hashing when creating a user."""
        password = request.data.get("password", None)
        if not password:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = make_password(password)

        # Optional: Add bcrypt salting
        salt = bcrypt.gensalt()
        hashed_with_salt_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        return Response({"message": "User created successfully", "hashed_password": hashed_password})

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]  # Only the user can modify their own account

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        """Retrieve a specific user's details (only the owner or an admin)."""
        user = self.get_object(pk)
        if not user:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the requesting user is the owner or an admin
        if request.user != user and not request.user.is_staff:  
            return Response({"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        """Allow only the owner to update their details."""
        user = self.get_object(pk)
        if not user:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, user)  # Enforce IsOwner permission

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            if "password" in request.data:
                user.password = make_password(request.data["password"])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Allow only the owner to delete their account."""
        user = self.get_object(pk)
        if not user:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, user)  # Enforce IsOwner permission

        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)        
        
class UserLogin(APIView):
    """Handles user authentication"""

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            #Log successful
            logger.info(f"User '{username}' logged in successfully.")
            # If user is authenticated, check if they're an admin
            if user.groups.filter(name="Admin").exists():
                token, created = Token.objects.get_or_create(user=user)  # Check if the user is in the Admin group
                return Response({"message":"Login Successful!"" --- Welcome, Admin!", "token": token.key}, status=status.HTTP_200_OK)

            # If not an admin, return a normal success message
            token, created = Token.objects.get_or_create(user=user)  # Fetch or create token
            return Response({
                "message": "Login successful!",
                "token": token.key  
            }, status=status.HTTP_200_OK)
        
        else:
            # Log failed login attempt
            logger.warning(f"Failed login attempt for username: {username}")
            return Response({"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        

class PostListCreate(APIView):#GENERAL, create a post, get ALL the posts
    permission_classes = [IsAuthenticated]
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


    def post(self, request):
        data = request.data

        try:
            post = PostFactory.create_post(
            post_type=data['post_type'],
            title=data['title'],
            content=data.get('content', ''),
            metadata=data.get('metadata', {}),
            author=request.user  # Automatically set the author to the logged-in user
        )

            # Return the response with the created post details
            return Response({'message': 'Post created successfully!', 'post_id': post.id}, status=status.HTTP_201_CREATED)

        except ValueError as e:
            # If the post type is invalid or missing metadata, handle the exception
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):#INDIVIDUAL, user needs to be authenticated first
    permission_classes = [IsAuthenticated, IsPostAuthor]

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        self.check_object_permissions(request, post)
        return Response({"content": post.content})
    
    def patch(self, request, pk):
        post = Post.objects.get(pk=pk)  # Get post by ID (pk)
        self.check_object_permissions(request, post)  # Ensure user is allowed to edit this post
        
        # Update only the fields that are passed in the request
        serializer = PostSerializer(post, data=request.data, partial=True)  # partial=True means not all fields need to be sent
        if serializer.is_valid():
            serializer.save()  # Save the updated post
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = Post.objects.get(pk=pk)  # Get post by ID (pk)
        self.check_object_permissions(request, post)  # Ensure user is allowed to delete this post
        
        post.delete()  # Delete the post
        return Response(status=status.HTTP_204_NO_CONTENT)  # Return 204 No Content on successful deletion

class CommentListCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only logged-in users can access

    def get(self, request, post_id):
        """Retrieve all comments for a specific post"""
        comments = Comment.objects.filter(post_id=post_id)  # Filter by post
        if not comments:
            return Response({"message": "No comments found for this post."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        """Create a new comment for a post"""
        try:
            post = Post.objects.get(id=post_id)  # Try to get the post by ID
        except Post.DoesNotExist:
            return Response({"message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)  # Automatically set author & post
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentDetailView(APIView):#SPECIFIC COMMENT
    permission_classes = [IsAuthenticated, IsCommentAuthor]

    def get(self, request, pk):
        """Retrieve a single comment."""
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def patch(self, request, pk):
        """Update a comment (only by author)."""
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)  # Enforces permission

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete a comment (only by author)."""
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)  # Enforces permission

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]  # Use the permission class to check access

    def get(self, request):
        return Response({"message": "Welcome, Admin!"})


