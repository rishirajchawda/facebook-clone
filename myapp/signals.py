from django.contrib.auth import user
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Relationship ,Profile

@receiver(post_save, sender = Relationship)
def post_save_add_to_friends(sender ,created, instance, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()