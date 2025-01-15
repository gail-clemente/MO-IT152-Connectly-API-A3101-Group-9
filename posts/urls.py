from django.urls import path
from . import views

urlpatterns = [
            path('users/', views.get_users, name='get_users'), # Get the users
            path('users/create/', views.create_user, name='create_user'), # Create a user
            path('users/update/<int:id>/', views.update_user, name='update_user'), # Update a user
            path('users/delete/<int:id>/', views.delete_user, name='delete_user'), # Delete a user
            path('posts/create/', views.create_post, name='create_posts'), # Create post
            path('posts/', views.get_posts, name='get_posts'), # Get posts

        ]