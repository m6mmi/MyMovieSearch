from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='static/img/profile_pictures', blank=True, null=True, default='placeholder.png')
    favorite_movies = models.JSONField(default=list)

    def is_movie_in_bookmarks(self, movie_id):
        is_in_list = any(str(movie['movie_id']) == str(movie_id) for movie in self.favorite_movies)
        return is_in_list
