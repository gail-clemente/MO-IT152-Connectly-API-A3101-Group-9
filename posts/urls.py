from django.urls import path
from . import views
from .views import AdminOnlyView, PostDetailView, UserListCreate, PostListCreate, CommentListCreate, UserLogin

urlpatterns = [
            #ADMIN
            path('admin/', AdminOnlyView.as_view(), name='admin'),
            #GENERAL-USERS
            path('users/', UserListCreate.as_view(), name='user-list-create'), # get users and post users
            #GENERAL-POSTS
            path('posts/', PostListCreate.as_view(), name='post-list-create'), # get and post 'posts'
            #INDIVIDUAL_POSTS
            path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
            #GENERAL-COMMENTS
            path('comments/', CommentListCreate.as_view(), name='comment-list-create'), # get & post comments
            #LOGIN
            path('users/login/', UserLogin.as_view(), name='user-login'),
            #path('users/', views.get_users, name='get_users'), # Get the users
            #path('users/create/', views.create_user, name='create_user'), # Create a user
            #path('users/update/<int:id>/', views.update_user, name='update_user'), # Update a user
            #path('users/delete/<int:id>/', views.delete_user, name='delete_user'), # Delete a user
            #path('posts/create/', views.create_post, name='create_posts'), # Create post
            #path('posts/', views.get_posts, name='get_posts'), # Get posts
        ]