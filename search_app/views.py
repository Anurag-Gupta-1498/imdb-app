import traceback
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .decorators import admin_user_required
from .serializers import MovieSerializer
from .models import MovieDetails
import rest_framework
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.utils import IntegrityError


# Create your views here.


@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated, ])
class MovieCreateDeleteUpdate(APIView):
    """
    Api for crud operations on database
    """

    def get(self, request, pk=None):
        movie = get_object_or_404(MovieDetails, id=pk)
        movie_serializers = MovieSerializer(instance=movie)
        return Response(movie_serializers.data, status=status.HTTP_200_OK)

    @method_decorator(admin_user_required)
    def post(self, request):
        try:
            movie_serializers = MovieSerializer(data=request.data)
            movie_serializers.is_valid(raise_exception=True)
            movie_serializers.save(data=request.data['genres'])
        except IntegrityError as e:
            return Response({'msg': 'movie already exists in database'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(movie_serializers.data, status=status.HTTP_201_CREATED)

    @method_decorator(admin_user_required)
    def put(self, request, pk=None):
        movie = get_object_or_404(MovieDetails, id=pk)
        movie_serializers = MovieSerializer(instance=movie, data=request.data)
        movie_serializers.is_valid(raise_exception=True)
        movie_serializers.save()
        return Response(movie_serializers.data, status=status.HTTP_200_OK)

    @method_decorator(admin_user_required)
    def delete(self, request, pk=None):
        movie = get_object_or_404(MovieDetails, id=pk)
        movie.delete()
        return Response({'msg': 'done'}, status=status.HTTP_200_OK)


@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated, ])
class SearchAPI(APIView):
    """
    SEARCH API for filtering movies on basis of movie name, director, rating, etc
    """

    @staticmethod
    def get(request):
        try:
            page = request.GET.get('page', 1)
            search_name = request.GET.get('search_name', '')
            search_director = request.GET.get('search_director', '')
            search_rating = request.GET.get('search_rating', '')
            search_popularity = request.GET.get('search_popularity', '')
            search_genre = request.GET.get('search_genre', '')
            paginator_len = request.GET.get('paginator_len', 10)
            paginator_req = request.GET.get('paginator_req', 'yes')

            try:
                page = int(page)
            except ValueError as e:
                return Response({'message': "Please enter valid number for page"},
                                status=rest_framework.status.HTTP_400_BAD_REQUEST)

            try:
                search_rating = int(search_rating)
            except ValueError as e:
                return Response({'message': "Please enter valid number for movie rating"},
                                status=rest_framework.status.HTTP_400_BAD_REQUEST)

            try:
                search_popularity = int(search_popularity)
            except ValueError as e:
                return Response({'message': "Please enter valid number for movie popularity"},
                                status=rest_framework.status.HTTP_400_BAD_REQUEST)

            try:
                paginator_len = int(paginator_len)
            except ValueError as e:
                return Response({'message': "Please enter valid number for paginator length"},
                                status=rest_framework.status.HTTP_400_BAD_REQUEST)

            if paginator_req.lower() not in ('yes', 'no'):
                return Response({'message': "Please enter valid option for paginator required - yes/no"},
                                status=rest_framework.status.HTTP_400_BAD_REQUEST)

            queryset = MovieDetails.objects.all().prefetch_related("genres").order_by('-id')
            if search_name:
                queryset = queryset.filter(
                    movie_name__icontains=search_name).order_by('-id')
            if search_director:
                if search_director != '' and queryset.filter(director__iexact=search_director).count() > 0:
                    queryset = queryset.filter(director__iexact=search_director)
                else:
                    return Response({'message': 'No data exists for this Director'},
                                    status=rest_framework.status.HTTP_400_BAD_REQUEST)
            if search_rating:
                if queryset.filter(imdb_rating__gte=search_rating).count() > 0:
                    queryset = queryset.filter(imdb_rating__gte=search_rating)
                else:
                    return Response({'message': 'No movies above this rating exists in the database'},
                                    status=rest_framework.status.HTTP_400_BAD_REQUEST)

            if search_popularity:
                if queryset.filter(movie_popularity__gte=search_popularity).count() > 0:
                    queryset = queryset.filter(movie_popularity__gte=search_popularity)
                else:
                    return Response({'message': 'No movies above this popularity exists in the database'},
                                    status=rest_framework.status.HTTP_400_BAD_REQUEST)

            if search_genre:
                if search_genre != '' and queryset.filter(genres__genre_name__iexact=search_genre).count() > 0:
                    queryset = queryset.filter(genres__genre_name__iexact=search_genre)
                else:
                    return Response({'message': 'No data exists for this Genre'},
                                    status=rest_framework.status.HTTP_400_BAD_REQUEST)

            if paginator_req.lower() == 'yes':
                paginator = Paginator(queryset, paginator_len)
                try:
                    queryset = paginator.page(page)
                except PageNotAnInteger:
                    queryset = paginator.page(1)
                except EmptyPage:
                    queryset = paginator.page(paginator.num_pages)

            if not queryset:
                message = 'No Data Found'

            if len(queryset) != 0:
                return Response(
                    {'message': 'Received successfully', 'data': list(MovieSerializer(queryset, many=True).data)},
                    status=rest_framework.status.HTTP_200_OK)
            else:
                return Response({'message': 'No data exists for the query'},
                                status=rest_framework.status.HTTP_400_BAD_REQUEST)

        except MovieDetails.DoesNotExist as e:
            message = 'Movie Details does not exist'
            status_code = 404


        except Exception as e:
            traceback.print_exc()
            message = str(e)
            status_code = 500

        return Response({'message': message}, status=status_code)
