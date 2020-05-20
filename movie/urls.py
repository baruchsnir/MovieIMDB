from django.contrib import admin
from django.urls import path
from . import views
from . import models
app_name='movie'
urlpatterns = [
    path('movies_list/', views.movies_list, name='movies_list'),
    path('actors_list/', views.actors_list, name='actors_list'),
    path('movie_detail/', views.movie_detail, name='movie_detail'),
    path('actor_detail/', views.actor_detail, name='actor_detail'),
    path('create_review/', views.create_review, name='create_review'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('add_actor/', views.add_actor, name='add_actor'),
    path('add_actor_to_movie/', views.add_actor_to_movie,name='add_actor_to_movie'),
    path('search/', views.searchmovieoractor, name='search'),
    path('commentslist/', views.commentslist, name='commentslist'),
]
