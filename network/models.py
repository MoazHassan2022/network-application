from django.contrib.auth.models import AbstractUser
from django.db import models


class Post(models.Model):
    text = models.TextField(max_length=1000, default="", blank=True)
    poster = models.CharField(max_length=64, default="")
    date = models.CharField(max_length=64, default="")
    realDate = models.DateTimeField(auto_now=True)
    likesCount = models.IntegerField(null=True, default=0)


class User(AbstractUser):
    followersCount = models.IntegerField(null=True, blank=True, default=0)
    followsCount = models.IntegerField(null=True, blank=True, default=0)
    posts = models.ManyToManyField(Post, blank=True, related_name="userPost")
    followsList = models.ManyToManyField("self", blank=True, related_name="users", symmetrical=False)
    LikedList = models.ManyToManyField(Post, blank=True, related_name="userLikes")