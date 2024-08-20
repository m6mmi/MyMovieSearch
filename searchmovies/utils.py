import os
import requests
from searchmovies.models import SearchResult


def search_movie(title):
    """
    Search for a movie by title.

    This function sends a GET request to the TMDB (The Movie Database) API to search for movies
    that match the given title.

    Parameters:
    title (str): The title of the movie to search for.

    Returns:
    list: A list of SearchResult instances if the request is successful.
    None: If the request fails, it prints an error message and returns None.
    """

    url = f"https://api.themoviedb.org/3/search/movie?query={title}&include_adult=true&language=en-US&page=1"

    headers = {"accept": os.getenv('TMDB_ACCEPT'), "Authorization": os.getenv('TMDB_AUTHORIZATION')}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print('Failed to fetch data:', response.status_code)
        return

    data = response.json()
    results = []
    for item in data.get('results', []):
        result = SearchResult(
            title=item.get('title'),
            overview=item.get('overview'),
            year=item.get('release_date'),
            genre=item.get('genre_ids'),
            poster_image=item.get('poster_path'),
            movie_id=item.get('id')
        )
        results.append(result)

    return results


if __name__ == '__main__':
    search_movie('The Matrix')
