# Display the detailed movie information, including title, year, genre, overview, cast, and poster image.


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
