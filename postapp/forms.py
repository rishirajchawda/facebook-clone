from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields
from .models import Post ,Comment


class Postform(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','yourpost','post_pic')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)