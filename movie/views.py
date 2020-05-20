from django.shortcuts import render , redirect
from .models import Movie , Actor ,Popularity,Act,Seen,Expect,Review
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.db.models import Q
from .MovieDB import MovieDB
from .forms import ReviewForm
from . import forms
import json
import math

# Create your views here.
def movies_list(request):
    page = 1
    year = 0
    genre = 0
    if request.method == 'GET':
        page = request.GET.get('page')
        year = request.GET.get('year')
        genre = request.GET.get('genres')  #&year={{year}}&genres={{genres}}
        review  = request.GET.get('review')
        title = request.GET.get('title')
        # if title:
        #     return search_string(request,title)
    if review:
       if review == True:
           return commentslist(request)

    if page is None:
        page = 1
    if year is None:
        year = 0
    if year == 'All':
        year = 0
    if genre is None:
        genre = 0
    if genre == 'All':
        genre = 0

    movies_in_line = 8
    page = int(page)
    objects = []
    objects1 = []
    print('genre', genre)
    print('year', year)
    movies = Movie.objects.all()
    print( 'movies',len(movies))
    if year == 0:
        objects1 = movies
    else:
        for obj in movies:
            if year in obj.year:
                objects1.append(obj)
    print('objects1', len(objects1))
    if genre != 0:
        for obj in objects1:
            if genre in obj.genres:
                objects.append(obj)
    else:
        objects = objects1
    if len(objects) == 0:
        return redirect('/')
    print('objects', len(objects))
    # print('Total Movies - ', len(objects))
    count_in_page = 10 * movies_in_line
    # print('count_in_page - ', count_in_page)
    total_page = int(math.ceil(len(objects) / count_in_page))
    if page > total_page:
        return render(request, '404.html')
    # print('total_page - ', total_page)

    last_item_index = count_in_page * page if page != total_page else len(objects)
    pages = []
    end_distance = total_page - page
    start_page_num = page - 5 if end_distance >= 5 else page - count_in_page + end_distance
    end_page_num = page + 5 if page > 5 else count_in_page
    for i in range(start_page_num, end_page_num + 1):
        if 1 <= i <= total_page:
            pages.append(i)
    data = {'items': objects[count_in_page * (page - 1):last_item_index], 'current_page': page,
            'page_number': total_page,
            'pages': pages, 'movies_in_line': movies_in_line,'review':False}
    years = get_years()
    genres = get_genres()
    data['years'] = years
    data['genres'] = genres
    data['year'] = year
    data['genre'] = genre

    return render(request, "movie/movie_list.html", data)


def commentslist(request):
    page = 1
    year = 0
    genre = 0
    if request.method == 'GET':
        page = request.GET.get('page')
        year = request.GET.get('year')
        genre = request.GET.get('genres')  #&year={{year}}&genres={{genres}}
        title = request.GET.get('title')
        # if title:
        #     return search_string(request,title)

    if page is None:
        page = 1
    if year is None:
        year = 0
    if genre is None:
        genre = 0
    movies_in_line = 8
    page = int(page)
    objects = []
    objects1 = []
    movies = []
    # print('genre', genre)
    # print('year', year)
    reviews = Review.objects.all()
    # print( 'reviews',len(reviews))
    for review in  reviews:
        if review.user == request.user:
            id = review.movieid
            print('id',id)
            if str(id) == "1":
                continue
            movie = Movie.objects.get(movieid=id)
            movies.append(movie)
    # print( 'movies',len(movies))
    if year == 0:
        objects1 = movies
    else:
        for obj in movies:
            if year in obj.year:
                objects1.append(obj)
    # print('objects1', len(objects1))
    if genre != 0:
        for obj in objects1:
            if genre in obj.genres:
                objects.append(obj)
    else:
        objects = movies
    if len(objects) == 0:
        return redirect('/')
    # print('objects', len(objects))
    # print('Total Movies - ', len(objects))
    count_in_page = 10 * movies_in_line
    # print('count_in_page - ', count_in_page)
    total_page = int(math.ceil(len(objects) / count_in_page))
    if page > total_page:
        return render(request, '404.html')
    # print('total_page - ', total_page)

    last_item_index = count_in_page * page if page != total_page else len(objects)
    pages = []
    end_distance = total_page - page
    start_page_num = page - 5 if end_distance >= 5 else page - count_in_page + end_distance
    end_page_num = page + 5 if page > 5 else count_in_page
    for i in range(start_page_num, end_page_num + 1):
        if 1 <= i <= total_page:
            pages.append(i)
    data = {'items': objects[count_in_page * (page - 1):last_item_index], 'current_page': page,
            'page_number': total_page,
            'pages': pages, 'movies_in_line': movies_in_line,'review':True}
    years = get_years()
    genres = get_genres()
    data['years'] = years
    data['genres'] = genres
    data['year'] = year
    data['genre'] = genre

    return render(request, "movie/movie_list.html", data)


def actors_list(request):
    page = 1
    if request.method == 'GET':
        page = request.GET.get('page')
        title = request.GET.get('title')
        # if title:
        #     return search_string(request,title)
    if not page:
        page = 1
    if page is None:
        return render(request, '404.html')
    movies_in_line = 8
    page = int(page)
    objects = Actor.objects.all()
    count_in_page = 10 * movies_in_line
    total_page = int(math.ceil(len(objects) / count_in_page))
    if page > total_page:
        return render(request, '404.html')

    last_item_index = count_in_page * page if page != total_page else len(objects)
    pages = []
    end_distance = total_page - page
    start_page_num = page - 5 if end_distance >= 5 else page - count_in_page + end_distance
    end_page_num = page + 5 if page > 5 else count_in_page
    for i in range(start_page_num, end_page_num + 1):
        if 1 <= i <= total_page:
            pages.append(i)
    data = {'items': objects[count_in_page * (page - 1):last_item_index], 'current_page': page, 'page_number': total_page,
            'pages': pages,'movies_in_line':movies_in_line}
    return render(request, "movie/actor_list.html", data)

def get_years():
    years = []
    year = 1
    new_list = ['All']
    movies = Movie.objects.all()
    for movie in movies:
        year = movie.year
        if year not in years:
            years.append(year)
    years.sort(reverse = True)
    for y in years:
        new_list.append(y)
    return new_list
def get_genres():
    genres = ['All']
    genre = ''
    movies = Movie.objects.all()
    for movie in movies:
        genre = movie.genres.split('|')
        for g in genre:
            if g not in genres:
                genres.append(g)
    return genres

@csrf_protect
def movie_detail(request):
    id = 1
    comments = []
    if request.method == 'GET':
        id = request.GET.get('id')
        title = request.GET.get('title')
        # if title:
        #     return search_string(request,title)
    print('id',id)
    if len(str(id)) < 4:
        return render(request, '404.html')
    items = []
    temp = ''
    try:
        try:
            movie = Movie.objects.get(movieid=id)
        except:
            movie = None
        print('movie', movie)
        if movie:
            try:
                # reviews = Review.objects.get(movieid=id)
                reviews = Review.objects.all()
                #print('reviews', reviews)
                if reviews:
                    for review in reviews:
                        #print('review.movieid',review.movieid)
                        temp = str(review.movieid).split('|')[0]
                        if temp != id:
                            continue
                        comments.append(review)
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print('Did not get Reviews',message)
            print('comments',comments)
            # print('movie - ' , movie)
            try:
                weight = movie.weight
                new_record = Popularity(movieid_id=id, weight=weight + 1)
                new_record.save()
            except:
                new_record = Popularity(movieid_id=id, weight=1)
                new_record.save()

            records = Act.objects.filter(movieid_id=id)
            if request.user.get_username() != '':
                seen_list = [str(x).split('|')[1] for x in
                             Seen.objects.filter(username=request.user.get_username())]
                expect_list = [str(y).split('|')[1] for y in
                               Expect.objects.filter(username=request.user.get_username())]
                if id in seen_list:
                    movie.flag = 1
                if id in expect_list:
                    movie.flag = 2
            # print('records',records)
            for query in records:
                for actor in Actor.objects.filter(actorid=query.actorid_id):
                    items.append(actor)
            # print('all data', {'items': items, 'number': len(items), 'movie': movie, 'comments': comments})
            return render(request, "movie/movie_detail.html",
                          {'items': items, 'number': len(items), 'movie': movie, 'comments': comments})
        else:
            return render(request, '404.html')
    except:
        return render(request, '404.html')

@csrf_protect
def actor_detail(request):
    id = 1
    if request.method == 'GET':
        id = request.GET.get('id')
        title = request.GET.get('title')
        # if title:
        #     return search_string(request,title)
    if not id:
        return render(request, '404.html')
    items = []
    try:
        label = 'movie'
        actor = Actor.objects.get(actorid=id)
        records = Act.objects.filter(actorid_id=id)
        for query in records:
            for movie in Movie.objects.filter(movieid=query.movieid_id):
                items.append(movie)
    except:
        return render(request, '404.html')
    return render(request, "movie/actor_detail.html",  {'items': items, 'number': len(items), 'actor': actor})


@csrf_protect
def create_review(request):
    id = 1
    title = 'stam'
    if request.method == 'GET':
        id = request.GET.get('id')
        movie = Movie.objects.get(movieid=id)
        title = movie.title
    if request.method  == "POST":
        rating = str(request.POST['rating']).strip()
        comment = str(request.POST['comment']).strip()
        id = str(request.POST['movieid']).strip()
        # save the article to DB
        movie = Movie.objects.get(movieid=id)
        #print('movie post', movie)
        try:
            review = Review()
            review.movieid = id
            review.user = request.user
            review.comment = comment
            review.rating = rating
            review.save()
        except Exception as ex:
            print('Exception' ,ex)

        #print('review',review)
        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        return redirect('/movie/movie_detail/?id='+str(id))
    return render(request, "movie/create_review.html",{'movieid':id,'title':title})

@csrf_protect
def add_movie(request):
    if request.method  == "POST":
        movieid = str(request.POST['movieid']).strip()
        title = str(request.POST['title']).strip()
        year = str(request.POST['year']).strip()
        length = str(request.POST['length']).strip()
        genres = str(request.POST['genres']).strip()
        poster = str(request.POST['poster']).strip()
        plot = str(request.POST['plot']).strip()
        trailer = str(request.POST['trailer']).strip()
        actors = str(request.POST['actors']).strip()
        rate = float(str(request.POST['rate']).strip())
        if ',' in genres:
            genres = genres.replace(",", "|")
        if ',' in genres:
            actors = actors.replace(",", "|")
        try:
            #Find if there is one, if not add it
            findmovie = False
            try:
                movie = Movie.objects.get(movieid=movieid)
                findmovie = True
                # print('movie in Data Base', movie)
            except:
                movie = None
            if findmovie == False:
                movie = Movie()
                movie.movieid = movieid
                movie.title = title
                movie.year = year
                movie.length = length
                movie.genres = genres
                movie.poster = poster
                movie.plot = plot
                movie.trailer = trailer
                movie.rate = rate
                movie.save()
                # print('movie', movie)
            #Add actors to Movie if there is actor in the Data Base
            countactors = 0
            if actors:
                if ',' in actors:
                    actorslist = actors.split(',')
                else:
                    actorslist = actors.split('|')
                # print('actorslist',actorslist)
                for a in actorslist:
                    a = str(a).strip()
                    newactor = None
                    try:
                        # print('a',a)
                        newactor = Actor.objects.get(name=a)
                    except:
                        newactor = None
                    #We Add Actor to Movie igf the actor is in the database
                    #We have to add first the actors so the adding of actor to this movie will be automaticly
                    if newactor:
                        countactors += 1
                        # print('actor - ' + str(countactors), newactor)
                        canadd = get_act_queryset(movie.movieid, newactor.actorid)
                        print('canadd', canadd)
                        if canadd == False:
                            act = Act()
                            act.movieid = movie
                            act.actorid = newactor
                            act.save()
#                            print('act',act)
        except Exception as ex:
            print('Exception' ,ex)


        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        return redirect('/movie/movie_detail/?id='+movieid)
    return render(request, "movie/create_movie.html")

@csrf_protect
def add_actor(request):
    if request.method == "POST":
        actorid = str(request.POST['actorid']).strip()
        name = str(request.POST['actorname']).strip()
        photo = str(request.POST['photo']).strip()
        # print('actorid',actorid)
        # print('name',name)
        # print('poto',photo)
        actor = None
        try:
            #Find if there is one, if not add it
            try:
                actor = Actor.objects.get(actorid=actorid)
            except:
                actor = None
            if not actor:
                actor = Actor()
                actor.actorid = actorid
                actor.name = name
                actor.photo = photo
                actor.save()
                # print('actor', actor)
        except Exception as ex:
            print('Exception', ex)


        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        return redirect('/movie/actor_detail/?id=' + str(actorid))
    return render(request   , "movie/create_actor.html")


def add_actor_to_movie(request):
    if request.method == "POST":
        actorid = str(request.POST['actorid']).strip()
        movieid = str(request.POST['movieid']).strip()
        try:


            try:
                movie = Movie.objects.get(movieid=movieid)
                actor = Actor.objects.get(actorid=actorid)
            except:
                actor = None
                movie = None
            messages = []
            if not movie:
                messages.append('There is no Movie with ID - ' + movieid)
            # else:
            #     print('movie', movie)
            if not actor:
                messages.append('There is no Actor with ID - ' + actorid)
            # else:
            #     print('actor', actor)
            print('messages = ',messages)
            if movie and actor:
                canadd = get_act_queryset(movie,actor)
                print('canadd',canadd)
                if not canadd:
                    act = Act()
                    act.actorid = actor
                    act.movieid = movie
                    act.save()
                    #print('act', act)
                else:
                    messages.append('There is a record of this match')
            else:
                render(request, "movie/add_actor_to_movie.html",{'message',messages})
        except Exception as ex:
            print('Exception', ex)


        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        return redirect('/movie/movie_detail/?id=' + str(movieid))
    return render(request, "movie/add_actor_to_movie.html")



def get_act_queryset(movieid,actorid):
    # print('Try ton get Act from', str(movieid) + ',' + str(actorid))
    command = 'SELECT * FROM movie_act WHERE actorid_id = \'{0}\' AND  movieid_id = \'{1}\''.format(actorid, movieid)
    db = MovieDB()
    rows = db.get_data_from_commans(command)
    # print('Data Rows from Act',rows)
    if len(rows) == 0:
        return False
    else:
        return True
    # object = Act.objects.filter(Q(movieid_id__icontains=movieid) & Q(actorid_id__icontains=actorid))
    # if object:
    #     return True
    # else:
    #     return False

def searchmovieoractor(request):
    try:
        if request.method == 'GET':
            query= request.GET.get('q')

            submitbutton= request.GET.get('submit')

            if query is not None:
                lookupsmovie= Q(title__icontains=query)
                lookupsactor = Q(name__icontains=query)
                movies= Movie.objects.filter(lookupsmovie).distinct()
                movie = None
                if movies:
                    if movies is Movie:
                        movie = movies
                    else:
                        movie = movies[0]
                    if movie:
                        print('movie', movie)
                        return redirect('/movie/movie_detail/?id=' + movie.movieid)
                else:
                    actors = Actor.objects.filter(lookupsactor).distinct()
                    if actors:
                        actor = None
                        if movies is Actor:
                            actor = actors
                        else:
                            actor = actors[0]
                        if actor:
                            print('actor', actor)
                            return redirect('/movie/actor_detail/?id=' + actor.actorid)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print('Did not get searchmovieoractor', message)
    return render(request, '404.html')
