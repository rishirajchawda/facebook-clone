from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=200, null=True, blank=True)
    yourpost = models.TextField(max_length=300, null=True, blank=True)
    post_pic = models.ImageField(upload_to="images/post_pic", null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked')
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Post by {}'.format(self.user)

    @property
    def number_of_likes(self):
        return self.likes.all().count()


def __str__(self):
    return str(self.user)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    content = models.CharField(max_length=1000, null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    class Meta:
        # sort comments in chronological order by default
        ordering = ('date_posted',)

    def __str__(self):
        return str(self.content)


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.post)
