from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Users)
class Users(admin.ModelAdmin):
    list_display = ('id', 'username', 'admin')
    search_fields = ('username',)


@admin.register(MovieGenre)
class MovieGenre(admin.ModelAdmin):
    list_display = ('id', 'genre_name')
    search_fields = ('genre_name',)


@admin.register(MovieDetails)
class MovieDetails(admin.ModelAdmin):
    list_display = ('id', 'movie_name', 'director', 'movie_popularity', 'imdb_rating')
    search_fields = ('movie_name', 'movie_popularity')
