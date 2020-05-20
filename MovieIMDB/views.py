from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from movie.models import Movie,Actor,Act,Popularity
import operator
import random
from movie.initializer import search_index

@csrf_protect
def index(request):
    data = {}
    movie_dict = search_index.data_in_memory['movie_dict']
    if request.user.is_authenticated:
        data = {'username': request.user.get_username()}
    if request.method == 'GET':
        title = request.GET.get('title')
        if title:
            return render(request, 'movie/search/?q=' + title)

    popular_movies = Popularity.objects.all().order_by('-weight')
    popular = []
    popular1 = []
    print('popular_movies',len(popular_movies))
    count = 0
    for movie in popular_movies:
        try:
            if count < 5:
                popular.append({'movieid': movie.movieid_id, 'title': movie_dict[movie.movieid_id].title,'poster': movie_dict[movie.movieid_id].poster})
            else:
                popular1.append({'movieid': movie.movieid_id, 'title': movie_dict[movie.movieid_id].title,'poster': movie_dict[movie.movieid_id].poster})
            count += 1
            if count >= 10:
                break

        except:
            continue

    data['popular'] = popular
    data['popular1'] = popular1
    #print(len(popular),len(popular1))
    # popular_movie_list = [movie_dict[movie.movieid_id] for movie in popular_movies[:5]]
    return render(request, 'base.html', data)
