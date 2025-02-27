from django.urls import path
from . import views
from .views import AdminOnlyView, CommentDetailView, CommentListCreateView, PostDetailView, UserDetailView, UserListCreateView, PostListCreate, UserLogin, PostLikeListView

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

            #Likes
            path('<int:post_id>/like/', PostLikeListView.as_view(), name='post-like-list-view' ),

        ]