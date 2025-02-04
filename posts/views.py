from argon2 import hash_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from posts import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
import bcrypt
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin, IsPostAuthor
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .permissions import IsAdmin  # Assuming you have this custom permission

User = get_user_model()



class ProtectedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        return Response({"message": "Authenticated!"})


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

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
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
            return Response({"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        

class PostListCreate(APIView):#GENERAL, create a post, get ALL the posts
    #permission_classes = [IsAuthenticated, IsPostAuthor]
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


    def post(self, request):
        print(request.data)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    
        
class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]  # Use the permission class to check access

    def get(self, request):
        return Response({"message": "Welcome, Admin!"})


