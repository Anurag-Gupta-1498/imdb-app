from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


# Create your models here.

def validate_interval_for_popularity(value):
    """
    Function to check value for popularity
    """
    if value < 0.0 or value > 100.0:
        raise ValidationError(('%(value)s must be in the range [0.0, 100.0]'), params={'value': value}, )


def validate_interval_for_ratings(value):
    """
    Function to check value for ratings
    """
    if value < 0.0 or value > 10.0:
        raise ValidationError(('%(value)s must be in the range [0.0, 10.0]'), params={'value': value}, )


class Users(AbstractUser):
    """
    Primary user model
    """
    admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class MovieGenre(models.Model):
    """
    Model to store genres of a movie
    """

    genre_name = models.TextField(unique=True, db_index=True)

    def __str__(self):
        return self.genre_name


class MovieDetails(models.Model):
    """
    Model to store movie details
    """

    movie_name = models.TextField(db_index=True)
    director = models.TextField(db_index=True)
    movie_popularity = models.FloatField(default=0.0, validators=[validate_interval_for_popularity])
    imdb_rating = models.FloatField(default=0.0, validators=[validate_interval_for_ratings])
    genres = models.ManyToManyField(MovieGenre, related_name='genre')

    def __str__(self):
        return self.movie_name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['movie_name', 'director'], name='unique_migration_host_combination'
            )
        ]