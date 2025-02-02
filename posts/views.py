from argon2 import hash_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from posts import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
import bcrypt


class UserListCreate(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        
        # You can now access the password from the request in POST method
        # If you were manually handling the password for verification or hash demonstration:
        password = request.data.get("password", None)  # This comes from the Postman request
        
        if password:
            # Hashing password using Django's make_password
            hashed_password = make_password(password)
            print("Hashed password:", hashed_password)  # Outputs a hashed version of the password

            # Verifying the hashed password
            isPasswordValid = check_password(password, hashed_password)
            print('Is the password valid? ', isPasswordValid)  # Outputs True if the password matches

        # Salting with bcrypt (optional)
        salt = bcrypt.gensalt()
        if password:
            hashWithSaltPassword = bcrypt.hashpw(password.encode('utf-8'), salt)
            print('Hash with salt password is: ', hashWithSaltPassword)
            
            # Verify a password
            if bcrypt.checkpw(password.encode('utf-8'), hashWithSaltPassword):
                print("Password is correct")
            else:
                print("Invalid password")
        
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Hash the password before saving the user, coming from the Postman request
            password = request.data["password"]
            hashed_password = make_password(password)  # Hash the password
            user = User.objects.create(
                username=serializer.validated_data["username"],
                email=serializer.validated_data.get("email", ""),
                password=hashed_password  # Save the hashed password
            )
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    """Handles user authentication"""

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            return Response({"message": "Authentication successful!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        

class PostListCreate(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListCreate(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        



