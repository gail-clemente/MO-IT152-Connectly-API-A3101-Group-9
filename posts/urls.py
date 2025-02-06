from django.urls import path
from . import views
from .views import AdminOnlyView, CommentDetailView, CommentListCreateView, PostDetailView, UserDetailView, UserListCreateView, PostListCreate, UserLogin

urlpatterns = [
            #ADMIN
            path('admin-only/', AdminOnlyView.as_view(), name='admin-only-view'),
            #ALL-USERS
            path('users/', UserListCreateView.as_view(), name='user-list-create'), # get users and post users
            #SPECIFICUSER-UPDATE&DELETE USER
            path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
            #NOAUTH-POSTS
            path('posts/', PostListCreate.as_view(), name='post-list-create'), # get and post 'posts'
            #NEEDAUTH_POSTS
            path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
            #ALL-COMMENTS
            path('<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'), # get & post all comments
            #SPECIFIC_COMMENT
            path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
            #LOGIN
            path('users/login/', UserLogin.as_view(), name='user-login'),
            #path('users/', views.get_users, name='get_users'), # Get the users
            #path('users/create/', views.create_user, name='create_user'), # Create a user
            #path('users/update/<int:id>/', views.update_user, name='update_user'), # Update a user
            #path('users/delete/<int:id>/', views.delete_user, name='delete_user'), # Delete a user
            #path('posts/create/', views.create_post, name='create_posts'), # Create post
            #path('posts/', views.get_posts, name='get_posts'), # Get posts
        ]