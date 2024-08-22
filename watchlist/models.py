from django.db import models
from django.contrib.auth.models import User


class WatchList(models.Model):
    movie_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    poster_image = models.CharField(max_length=255, default='')
    user_id = models.ManyToManyField(User, related_name='movies')
