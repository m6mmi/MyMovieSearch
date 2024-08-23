from django.contrib.auth.models import User
from django.db import models



class MovieDetailsResult:
    objects = None

    def __init__(self, title, year, genre, overview, poster_image, movie_id):
        self.title = title
        self.year = year
        self.overview = overview
        self.genre = genre
        self.poster_image = poster_image
        self.movie_id = movie_id

class Cast:
    def __init__(self, name, character):
        self.name = name
        self.character = character


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    movie_id = models.IntegerField()
    rating = models.IntegerField()
    comment = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
