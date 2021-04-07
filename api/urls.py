from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('profile-list/', views.ProfileList.as_view(), name="profile-list"),
    path('profile-add/', views.ProfileAdd.as_view(), name="profile-add"),
    path('profile-show/<int:pk>/', views.ProfileShow.as_view(), name="profile-show"),
    path('profile-update/<int:pk>/', views.ProfileUpdate.as_view(), name="profile-update"),
    path('profile-delete/<int:pk>/', views.ProfileDestroy.as_view(), name="profile-delete"),
    path('user-add/', views.UserAdd.as_view(), name="user-add"),
    path('comment-add/', views.CommentAdd.as_view(), name="comment-add"),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('post-add/', views.PostCreate.as_view(), name="post-add"),
    path('post-update/<int:pk>/', views.PostUpdate.as_view(), name="post-update"),
    path('post-list/', views.PostList.as_view(), name="post-list"),
    path('post-delete/<int:pk>/', views.PostDelete.as_view(), name="post-delete"),
    path('friend-list/', views.FriendList.as_view(), name="post-list"),
    path('friend-rec/', views.FriendRec.as_view(), name="friend-rec"),

]
