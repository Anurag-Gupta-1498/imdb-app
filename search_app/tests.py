from django.test import TestCase
from django.urls import reverse
from rest_framework.test import force_authenticate
from rest_framework import status
from rest_framework.test import APIRequestFactory
# from .views import MovieCreateDeleteUpdate, SearchAPI
from .models import MovieGenre, Users, MovieDetails
import json
from .create_users import create_users
from .urls import *
from .load_json import load_movies_data

# Create your tests here.

class TestApp(TestCase):
    """
    Unit test cases for different apis and functions.
    """

    def setUp(self):
        """
        Setting variables for testing
        """
        self.user = Users.objects.create_user(username='Anurag1', password='Anurag@123', admin=True)
        self.user2 = Users.objects.create_user(username='Anurag2', password='Anurag@123', admin=False)
        self.request_factory = APIRequestFactory()
        self.movies_url_create = reverse("movies_create")
        self.movies_url_delete = reverse("movies_delete", kwargs={'pk': 1})
        self.movies_url_update = reverse("movies_update", kwargs={'pk': 248})
        self.movies_url_search = reverse("search_movie")
        self.cud_view = MovieCreateDeleteUpdate.as_view()
        self.search_view = SearchAPI.as_view()
        self.movie = MovieDetails.objects.create(movie_name="Spider Man", director="Nolan")
        self.movies = self.test_load_movies()
    def test_create_users(self):
        """
        To test create user function
        """
        self.assertEqual(create_users(), "Users are created")

    def test_load_movies(self):
        """
        To test load movies function
        """
        self.assertEqual(load_movies_data(), "File loaded Successfully")

    def test_create_movies_admin_user(self):
        """
        To test create movies api
        """
        data = {
            "movie_popularity": 13,
            "director": "Dennis Donnelly",
            "genres": [
                "Action",
                "Comedy",
                "Romantic"
            ],
            "imdb_rating": 3,
            "movie_name": "Charlies Angels 4"
        }
        headers = {"Content-Type": "application/json"}
        request = self.request_factory.post(self.movies_url_create, data=data, headers=headers, verify=False)
        force_authenticate(request, user=self.user)
        response = self.cud_view(request)

        assert response.status_code == status.HTTP_201_CREATED


    def test_create_movies_non_admin_user(self):
        """
        To test create movies api
        """
        data = {
            "movie_popularity": 13,
            "director": "Dennis Donnelly",
            "genres": [
                "Action",
                "Comedy",
                "Romantic"
            ],
            "imdb_rating": 3,
            "movie_name": "Charlies Angels 4"
        }
        headers = {"Content-Type": "application/json"}
        request = self.request_factory.post(self.movies_url_create, data=data, headers=headers, verify=False)
        force_authenticate(request, user=self.user2)
        response = self.cud_view(request)
        response.render()
        json_response = json.loads(response.content)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert json_response["detail"] == "You do not have permission to perform this action."

    def test_update_movies(self):
        """
        To test update movie api
        """
        data = {
            "movie_popularity": 21,
            "director": "Dennis Donnelly",
            "imdb_rating": 3,
            "movie_name": "Charlies Angels 8"
        }
        headers = {"Content-Type": "application/json"}
        request = self.request_factory.put(self.movies_url_update, data=data, headers=headers, verify=False)
        force_authenticate(request, user=self.user)
        response = self.cud_view(request, pk=1)

        assert response.status_code == status.HTTP_200_OK

    def test_delete_movies(self):
        """
        To test delete movie api
        """
        request = self.request_factory.delete(self.movies_url_delete, verify=False)
        force_authenticate(request, user=self.user)
        response = self.cud_view(request, pk=1)

        assert response.status_code == status.HTTP_200_OK

    def test_search_movies(self):
        """
        To test search movie api
        """
        request = self.request_factory.get(self.movies_url_search)
        force_authenticate(request, user=self.user)
        response = self.search_view(request)
        response.render()
        json_response = json.loads(response.content)
        assert response.status_code == status.HTTP_200_OK
        assert len(json_response['data']) == 10

    def test_search_movies_name(self):
        """
        To test search movie api
        """
        data = {"search_name": "spider"}
        request = self.request_factory.get(self.movies_url_search, data=data)
        force_authenticate(request, user=self.user)
        response = self.search_view(request)
        response.render()
        json_response = json.loads(response.content)
        assert response.status_code == status.HTTP_200_OK
        assert len(json_response['data']) == 1
        assert json_response['data'][0]['movie_name'].lower() == "spider man"

    def test_search_movies_director(self):
        """
        To test search movie api
        """
        data = {"search_director": "nolan"}
        request = self.request_factory.get(self.movies_url_search, data=data)
        force_authenticate(request, user=self.user)
        response = self.search_view(request)
        response.render()
        json_response = json.loads(response.content)
        assert response.status_code == status.HTTP_200_OK
        assert len(json_response['data']) == 1
        assert json_response['data'][0]['movie_name'].lower() == "spider man"
        assert json_response['data'][0]['director'].lower() == "nolan"

    def test_search_movies_director_wrong(self):
        """
        To test search movie api
        """
        data = {"search_director": "a"}
        request = self.request_factory.get(self.movies_url_search, data=data)
        force_authenticate(request, user=self.user)
        response = self.search_view(request)
        response.render()
        json_response = json.loads(response.content)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert json_response['message'] == 'No data exists for this Director'

    def test_search_movies_name_director(self):
        """
        To test search movie api
        """
        data = {"search_name": "spider", "search_director": "nolan"}
        request = self.request_factory.get(self.movies_url_search, data=data)
        force_authenticate(request, user=self.user)
        response = self.search_view(request)
        response.render()
        json_response = json.loads(response.content)
        assert response.status_code == status.HTTP_200_OK
        assert len(json_response['data']) == 1
        assert json_response['data'][0]['movie_name'].lower() == "spider man"
        assert json_response['data'][0]['director'].lower() == "nolan"

    def test_search_movies_director_rating_wrong(self):
        """
        To test search movie api
        """
        data = {"search_name": "spider", "search_director": "nolan", "search_popularity": 90}
        request = self.request_factory.get(self.movies_url_search, data=data)
        force_authenticate(request, user=self.user)
        response = self.search_view(request)
        response.render()
        json_response = json.loads(response.content)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert json_response['message'] == 'No movies above this popularity exists in the database'


    def test_check_paginator(self):
        """
        To test search movie api
        """
        data = {"paginator_len": 20}
        request = self.request_factory.get(self.movies_url_search, data=data)
        force_authenticate(request, user=self.user)
        response = self.search_view(request)
        response.render()
        json_response = json.loads(response.content)
        assert response.status_code == status.HTTP_200_OK
        assert len(json_response['data']) == 20