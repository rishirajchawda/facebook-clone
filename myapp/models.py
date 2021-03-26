from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save ,pre_delete
from django.dispatch import receiver
from django.db.models import Q

GENDER_CHOICES = (
    ("MALE", "male"),
    ("FEMALE", "female"),
    ("OTHER", "other"),
    )


class ProfileManager(models.Manager):

    def get_all_profile_to_invite(self , sender):
        profiles = Profile.objects.all().exclude(user = sender)
        profile = Profile.objects.get(user = sender)
        qs = Relationship.objects.filter(Q(sender = profile) | Q(receiver = profile))
        print(qs)

        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        print(accepted)

        available = [profile for profile in profiles if profile not in accepted]
        print(available)
        return available

    def get_all_profiles(self , me):
        profiles = Profile.objects.all().exclude(user = me)
        return profiles


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
    friends = models.ManyToManyField(User , related_name='friends', blank=True)

    objects = ProfileManager()

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def __str__(self):
        return str(self.user)  

@receiver(post_save ,sender=User)
def Profile_update(sender ,instance , created ,**kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


STATUS_CHOICES = (
    ('send' , 'send'),
    ('accepted' , 'accepted'),
)


class RelationshipManager(models.Manager):
    def invatations_received(self ,receiver):
        qs = Relationship.objects.filter(receiver = receiver ,status = 'send')
        return qs 

class Relationship(models.Model): 
    sender = models.ForeignKey(Profile , on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile , on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8 , choices = STATUS_CHOICES)
    updated = models.DateField(auto_now = True)
    created = models.DateField(auto_now_add = True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"

@receiver(post_save, sender = Relationship)
def post_save_add_to_friends(sender ,created, instance, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()

@receiver(pre_delete , sender=Relationship)
def pre_delete_remove_from_friends(sender ,instance , **kwargs ):
    sender = instance.sender
    receiver = instance.receiver

    sender.friends.remove(receiver.user)
    receiver.friends.remove(sender.user)

    sender.save()
    receiver.save()