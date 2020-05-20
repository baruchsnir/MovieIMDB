from django.db.models import Q
from movie.models import  Movie,Actor,Act
from .MngIMDB import MngIMDB ,moviedata
movie_list = []
mng = MngIMDB()
movie_list = mng.load_data_from_csv()
mng.setUpClass()

for movie in movie_list:
    lookupsmovietitle = Q(title__icontains=movie.title)
    lookupsmovieid = Q(movieid__icontains=movie.movieid)
    movies = Movie.objects.filter(lookupsmovietitle | lookupsmovieid).distinct()
    if movies:
        continue
    newmovie = Movie()
    newmovie.title = movie.title
    newmovie.rate = movie.rate
    newmovie.year = movie.year
    genres = str(movie.genres)
    newmovie.genres =  genres.replace(",", "|")
    newmovie.plot = movie.plot
    newmovie.length = movie.length
    results = mng.search_movie(movie.title)
    newmovie.poster = results['']
    newmovie.trailer = results['trailer']
    newmovie.movieid = results['movieid']
    newmovie.poster = results['poto']
    newmovie.rate = results['rateing']
    newmovie.save()
    actors = str(movie.actors).split(',')
    for act in actors:
        a = act.strip()
        lookupsactname = Q(name__icontains=a)
        acs = Actor.objects.filter(lookupsactname).distinct()
        if acs:
            continue
        results = mng.search_actor(a)
        newactor = Actor()
        newactor.name = a
        newactor.photo = results['poto']
        newactor.actorid = results['actorid']
        newactor.save()
        act = Act()
        act.movieid = newmovie
        act.actorid = newactor
        act.save()

mng. tearDownClass()


