from rest_framework import serializers
from myapp.models import Profile, Relationship
from django.contrib.auth.models import User
from postapp.models import Comment
from postapp.models import Post


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'first_name', 'last_name', 'gender', 'email']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class CommentSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(source='user.username')
    # post = serializers.CharField(source='post.id')
    class Meta:
        model = Comment
        fields = ['post', 'user', 'content', 'date_posted']


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'yourpost', 'post_pic', 'date_posted']


class FriendsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = ['id', 'user', 'friends']


class FriendsReceivedSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Relationship
        fields = ['id', 'user', 'receiver', 'sender']
