from django.urls import path
from .views import *



urlpatterns = [
    path('movies_create/', MovieCreateDeleteUpdate.as_view(), name='movies_create'),
    path('movies_update/<int:pk>', MovieCreateDeleteUpdate.as_view(), name='movies_update'),
    path('movies_delete/<int:pk>', MovieCreateDeleteUpdate.as_view(), name='movies_delete'),
    path('search_movie/', SearchAPI.as_view(), name='search_movie'),
]