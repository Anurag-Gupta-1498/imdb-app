from rest_framework import serializers
from .models import MovieGenre, MovieDetails
from django.core.exceptions import ValidationError

class MovieGenreSerializer(serializers.ModelSerializer):
    """
    Serializer for genre model
    """

    class Meta:
        model = MovieGenre
        fields = ['genre_name']


class MovieDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Movie model
    """
    genres = MovieGenreSerializer(many=True, read_only=True)

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


class ValidationSerializer(serializers.Serializer):
    page = serializers.IntegerField(default=1)
    search_name = serializers.CharField(default=None)
    search_director = serializers.CharField(default=None)
    search_rating = serializers.IntegerField(default=None)
    search_popularity = serializers.IntegerField(default=None)
    search_genre = serializers.CharField(default=None)
    paginator_len = serializers.IntegerField(default=10)
    paginator_req = serializers.ChoiceField(default='yes', choices=(('yes', 'yes'), ('no', 'no')))