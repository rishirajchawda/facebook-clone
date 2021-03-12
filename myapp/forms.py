from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class Fbform(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Fist Name' )
    last_name = forms.CharField(max_length=100, help_text='Last Name' ) 
    email = forms.EmailField(max_length=150 , help_text='Your email' )

    class Meta:
        model = User 
        fields = ('username','first_name','last_name','email', 'password1','password2')
 
class ImageForm(forms.ModelForm):

    class Meta:
        model = Profile 
        fields = ('image',)

class ExtendForm(forms.ModelForm):

    class Meta:
        model = Profile 
        fields = ('gender',)

class UpdateForm(forms.ModelForm):

    class Meta:
        model = Profile 
        fields = ('first_name','last_name','email')

class UploadDP(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('image',)


class UploadBanner(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('banner_image',)

