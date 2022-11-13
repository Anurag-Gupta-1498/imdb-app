from imdbapp.settings import BASE_DIR
import traceback
import json
import os
from search_app.models import MovieGenre, MovieDetails

def load_movies_data():
    try:
        file_path = os.path.join(BASE_DIR, 'imdb.json')

        with open(file_path) as file:
            movies_data = eval(file.read())

        for movie_detail in movies_data:
            movie_object, _ = MovieDetails.objects.get_or_create(movie_name=movie_detail["name"].strip(),
                                                                 director=movie_detail["director"].strip(),
                                                                 movie_popularity=movie_detail["99popularity"],
                                                                 imdb_rating=movie_detail["imdb_score"])

            genres_movie = movie_detail["genre"]
            for genre in genres_movie:
                genre_object, _ =  MovieGenre.objects.get_or_create(genre_name=genre.strip())
                movie_object.genres.add(genre_object)

        return "File loaded Successfully"

    except FileNotFoundError as e:
        return "file is not present in the directory"

    except Exception as e:
        traceback.print_exc()
        return "exception found"


