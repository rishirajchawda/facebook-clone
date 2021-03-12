from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

GENDER_CHOICES = (
    ("MALE", "male"),
    ("FEMALE", "female"),
    ("OTHER", "other"),
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=150, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.CharField(max_length=100 ,null=True, blank=True)
    gender = models.CharField(max_length=111,choices=GENDER_CHOICES)
    image = models.ImageField(upload_to="images/post_pic",null=True,blank=True)
    banner_image = models.ImageField(upload_to="images/post_pic",null=True,blank=True)

    def __str__(self):
        return str(self.user)

@receiver(post_save ,sender=User)
def Profile_update(sender ,instance , created ,**kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


