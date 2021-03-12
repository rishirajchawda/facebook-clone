from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserPost


class Postform(forms.ModelForm):

    class Meta:
        model = UserPost
        fields = ('title','yourpost','post_pic')