from rest_framework import serializers
from .models import MovieGenre, MovieDetails


class GenreSerializer(serializers.ModelSerializer):
    """
    Serializer for genre model
    """

    class Meta:
        model = MovieGenre
        fields = ['genre_name']


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for Movie model
    """
    genres = GenreSerializer(many=True, read_only=True)

    def create(self, validated_data):
        genres_list = validated_data.pop('data')
        movie_obj = MovieDetails.objects.create(**validated_data)
        movie_obj.save()

        for genre in genres_list:
            genre_obj, _ = MovieGenre.objects.get_or_create(genre_name=genre)
            movie_obj.genres.add(genre_obj)
        return movie_obj

    class Meta:
        model = MovieDetails
        fields = ['movie_name', 'director', 'movie_popularity', 'imdb_rating', 'genres']
