from django.contrib.auth import get_user

from .serializers import ProfileSerializer, \
    UserSerializer, CommentSerializer, \
    PostSerializer, FriendsSerializer, FriendsReceivedSerializer
from myapp.models import Profile, Relationship
from postapp.models import Comment, Post
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import LoginUserPermission
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.models import Token
from django.http import Http404
from rest_framework import status


class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # def list(self, request):
    #     # TODO
    #     # Note the use of `get_queryset()` instead of `self.queryset`
    #     queryset = self.get_queryset()
    #     serializer = UserSerializer(queryset, many=True)
    #     return Response(serializer.data)


class ProfileAdd(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileShow(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileUpdate(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDestroy(generics.DestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserAdd(generics.CreateAPIView):
    # TODO
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CommentAdd(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, LoginUserPermission)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostUpdate(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, LoginUserPermission)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDelete(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, LoginUserPermission)


class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)


class FriendList(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        # if get_user(request.user.id):
        profile = Profile.objects.all()
        serializer = FriendsSerializer(profile, many=True)
        return Response(serializer.data)


class FriendRec(APIView):
    # permission_classes = (IsAuthenticated, LoginUserPermission)

    @staticmethod
    def get(request):
        # if get_user(request.user.id):
        profile = Relationship.objects.all()
        serializer = FriendsReceivedSerializer(profile, many=True)
        return Response(serializer.data)

# class FriendList(generics.ListAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = FriendsSerializer
#     permission_classes = (IsAuthenticated,)

# class PostCreate(APIView):
#     # permission_classes = IsOwnerOrReadOnly
#     def post(self, request, format=None):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def ApiList(request):
#     urlslink = {
#         # 'users_profile_list': reverse('profile-list', request=request, format=format),
#         'users_profile_create': reverse('profile-add', request=request, format=format),
#         # 'profile-show': reverse('profile-show', request=request, format=format),
#         # 'profile-update': reverse('profile-update', request=request, format=format),
#         # 'profile-delete"': reverse('profile-delete"', request=request, format=format),
#         'user-add': reverse('user-add', request=request, format=format),
#         'comment-add"': reverse('comment-add', request=request, format=format),
#         'post-add': reverse('post-add', request=request, format=format),
#         # 'post-update': reverse('post-update"', request=request, format=format),
#         'post-list': reverse('post-list', request=request, format=format),
#         # 'post-delete': reverse('post-delete', request=request, format=format),
#
#     }
#     return Response(urlslink)

# for user in User.objects.all():
#     Token.objects.get_or_create(user=user)
#
# class CommentAdd(APIView):
#     """
#     List all Comments, or create a new Comments.
# renderer_classes = [TemplateHTMLRenderer]

#     """

#     def get(self, request, format=None):
#         comments = Comment.objects.all()
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
