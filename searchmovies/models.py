from django.db import models

# Create your models here.
# title, year, genre, overview, and poster image
class SearchResult:
    def __init__(self, title, year, genre, overview, poster_image, movie_id):
        self.title = title
        self.year = year
        self.overview = overview
        self.genre = genre
        self.poster_image = poster_image
        self.movie_id = movie_id
