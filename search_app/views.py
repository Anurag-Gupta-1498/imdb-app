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
from .serializers import MovieDetailSerializer, ValidationSerializer
from .models import MovieDetails
import rest_framework
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.utils import IntegrityError
from .utils import get_name, get_rating, get_genre, get_director, get_popularity
# Create your views here.

functions_map = {'search_name': get_name, 'search_director': get_director, 'search_rating': get_rating,
                 'search_popularity': get_popularity, 'search_genre': get_genre}

@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated, ])
class MovieCreateDeleteUpdate(APIView):
    """
    Api for crud operations on database
    """
    def get(self, request, pk=None):
        movie = get_object_or_404(MovieDetails, id=pk)
        movie_serializers = MovieDetailSerializer(instance=movie)
        return Response(movie_serializers.data, status=status.HTTP_200_OK)

    @method_decorator(admin_user_required)
    def post(self, request):
        try:
            movie_serializers = MovieDetailSerializer(data=request.data)
            movie_serializers.is_valid(raise_exception=True)
            movie_serializers.save(data=request.data['genres'])
        except IntegrityError as e:
            return Response({'msg': 'movie already exists in database'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(movie_serializers.data, status=status.HTTP_201_CREATED)

    @method_decorator(admin_user_required)
    def put(self, request, pk=None):
        movie = get_object_or_404(MovieDetails, id=pk)
        movie_serializers = MovieDetailSerializer(instance=movie, data=request.data)
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
            request_params = request.GET
            validated_data = ValidationSerializer(data=request_params)
            if not validated_data.is_valid():
                return Response(validated_data.errors, status=rest_framework.status.HTTP_400_BAD_REQUEST)

            queryset = MovieDetails.objects.prefetch_related("genres").all().order_by('-imdb_rating')

            for data in validated_data:
                if data.value and data.name in functions_map:
                    queryset = functions_map[data.name](data.value, queryset)
                    if isinstance(queryset, dict):
                        return Response(queryset, status=rest_framework.status.HTTP_400_BAD_REQUEST)

            if validated_data['paginator_req'].value == 'yes':
                paginator = Paginator(queryset, validated_data['paginator_len'].value)
                try:
                    queryset = paginator.page(validated_data['page'].value)
                except PageNotAnInteger:
                    queryset = paginator.page(1)
                except EmptyPage:
                    queryset = paginator.page(paginator.num_pages)

            if len(queryset) != 0:
                return Response(
                    {'message': 'Received successfully', 'data': list(MovieDetailSerializer(queryset, many=True).data)},
                    status=rest_framework.status.HTTP_200_OK)
            else:
                return Response({'message': 'No Movies found'},
                                status=rest_framework.status.HTTP_400_BAD_REQUEST)

        except MovieDetails.DoesNotExist as e:
            message = 'Movie Details does not exist'
            status_code = 404

        except Exception as e:
            message = str(e)
            status_code = 500

        return Response({'message': message}, status=status_code)

