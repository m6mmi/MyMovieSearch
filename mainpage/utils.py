import json
import os
import requests

# temporary solution to load environment variables
from dotenv import load_dotenv
load_dotenv()


def current_movie_list():
    url = f"https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"

    headers = {"accept": os.getenv('TMDB_ACCEPT'), "Authorization": os.getenv('TMDB_AUTHORIZATION')}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print('Failed to fetch data:', response.status_code)
        return

    data = response.json()

    result_list = []

    for movie in data['results']:
        movie_id = movie['id']
        title = movie['title']
        poster_path = movie['poster_path']
        result_list.append({'id': movie_id, 'title': title, 'poster_path': poster_path})

    return result_list



if __name__ == '__main__':
    print(json.dumps(current_movie_list(), indent=4))
