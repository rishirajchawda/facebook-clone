from django.db import models
from django.contrib.auth.models import User

class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)

    title = models.CharField(max_length=200,null=True, blank=True)
    yourpost = models.TextField(max_length=300 ,null=True, blank=True)
    post_pic=models.ImageField(upload_to="images/post_pic",null=True,blank=True)
    

def __str__(self):
        return str(self.user) 