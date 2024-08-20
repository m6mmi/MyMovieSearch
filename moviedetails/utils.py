import os

import requests

from moviedetails import models

headers = {"accept": os.getenv('TMDB_ACCEPT'), "Authorization": os.getenv('TMDB_AUTHORIZATION')}

def details_movie(movie_id):
    url_movie = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

    response_movie = requests.get(url_movie, headers=headers)

    if response_movie.status_code != 200:
        print('Failed to fetch data:', response_movie.status_code)
        return

    data = response_movie.json()

    genres = [genre['name'] for genre in data.get('genres', [])]

    movie_detail_result = models.MovieDetailsResult(
        title=data.get('original_title'),
        year=data.get('release_date'),
        genre=genres,
        overview=data.get('overview'),
        poster_image=data.get('poster_path'),
        movie_id=data.get('id')
    )

    return movie_detail_result


def cast_list(movie_id):
    url_cast = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US"

    response_cast = requests.get(url_cast, headers=headers)

    if response_cast.status_code != 200:
        print('Failed to fetch data:', response_cast.status_code)
        return

    data = response_cast.json()

    cast = []
    for item in data.get('cast', []):
        cast_member = models.Cast(
            name=item.get('name'),
            character=item.get('character')
        )
        cast.append(cast_member)

    return cast


if __name__ == '__main__':
    details_movie(603)
    cast_list(603)