from Tests.MngIMDB import MngIMDB , moviedata
from Tests.MovieDB import MovieDB
from imdbpie import Imdb
import psutil

PROCNAME = "chromedriver.exe"

for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == PROCNAME:
        proc.kill()
def single_quote(string):
    s = str(string)
    if len(s) == 0:
        return 'None'
    try:
        if s.find('\'') != -1:
            return s.replace("\'", "\'\'")
        else:
            return s
    except Exception as ex:
        print('Exception at single_quote 22',ex)
        return s
movie_list = []
mng = MngIMDB()
movie_list = mng.load_data()
mngDb = MovieDB()
moviesid = mngDb.get_all_old_movies_by_field('movieid')
moviesnames = mngDb.get_all_old_movies_by_field('title')
actorsnames = mngDb.get_all_old_actors_by_field('name')
mng.setUpClass()
imdb = Imdb()
for movie in movie_list:
    if int(movie.year) < 2017:
        continue
    # for movie.title in moviesnames:
    #     continue
    try:
        if type(movie.title) is tuple:
            movie.title = movie.title[0]
        datam = None
        try:
            datam = imdb.search_for_title(movie.title)
        except:
            print("error")
            continue
        movie_id = ''
        print('Manage Movie',datam)
        try:
            for dic in datam:
                if str(dic['title']).lower() == movie.title.lower():
                    movie_id = dic['imdb_id']
                    break

            imdbmovie = imdb.get_title(movie_id)
            # datam.
            #
            # title = imdb.get_title(movie_id)
            # sql = (
            #     '''INSERT INTO movie_movie VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'''.format(
            #         movie_id,
            #         single_quote(str(title['base']['title'])),
            #         title['base']['year'],
            #         title['base']['runningTimeInMinutes'],
            #         movie_genres[movie_id],
            #         title['ratings']['rating'],
            #         single_quote(title['base']['image']['url']),
            #         single_quote(str(title['plot']['outline']['text'])),
            #         single_quote(str(imdb.get_title_videos(movie_id)['videos'][0]['encodings'][0]['play']))
            # movie_res =  mng.search_movie(movie.title)
            # movie_res['name'] = single_quote(movie.title)
            # movie.rate = movie_res['rate']
            # movie.plot = single_quote(movie.plot)
            # movie.trailer = single_quote(movie_res['trailer'])
            # movie.poster =  single_quote(movie_res['picurl'])
            # movie.title = single_quote(movie.title)
            # movie_id = movie_res['movieid']
            # movie.movieid = movie_id
            # print('Add Movie id ', movie_id)


            movie.rate = imdbmovie['ratings']['rating']
            movie.plot = single_quote(movie.plot)
            movie.trailer = single_quote(str(imdb.get_title_videos(movie_id)['videos'][0]['encodings'][0]['play']))
            movie.poster =  single_quote(imdbmovie['base']['image']['url'])
            movie.title = single_quote(movie.title)
            movie.movieid = movie_id
            print('Add Movie id ', movie_id)
            if mngDb.add_movie(movie):
                moviesnames.append(movie.title)
        except Exception as ex1:
            print('Exception at 51',ex1)

        actors_imdb = imdb.get_title_credits(movie_id)
        actor_length = len(actors_imdb['credits']['cast'])
        print('Add Actors: ', end='')
        actors = str(movie.actors).split(',')
        for actor in actors_imdb['credits']['cast'][:5 if actor_length > 5 else actor_length]:
            name = str(single_quote(str(actor['name'])))
            if name in actorsnames:
                continue
            print('Manage Actor', actor)
            actor_id = str(actor['id'].split('/')[2])
            try:
                url = str(single_quote(str(actor['image']['url'])))
            except:
                url = ''

            results = {}
            results['actorid'] = actor_id
            results['name']  = single_quote(name)
            results['picurl'] = single_quote(url)
            print('Add Actor', actor)
            mngDb.add_actor(results)
            print('Add Actor to movie', movie_id +" - " + actor_id)
            mngDb.add_act(movie_id,actor_id)
    except Exception as ex:
        print('Exception',ex)

mng.tearDownClass()





