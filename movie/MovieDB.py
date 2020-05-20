import sqlite3
#from Tests.MngIMDB import moviedata

class MovieDB():
    def sql_connection(self):
        try:
            con = sqlite3.connect('c:\\temp\\movie.db')
            #print("Connection is established: Database is created in memory")
            return con
        except Exception as Error:
            print(Error)

    def execute_sql(self,command):
        try:
            con = self.sql_connection()
            with con:
                cur = con.cursor()
            results = cur.execute(command)
            con.commit()
            return results
        except Exception as Error:
            print(Error)
        finally:
            con.close()

    def add_movie(self,movie):
        command = 'SELECT * FROM movie_movie WHERE movieid = \'{0}\''.format(movie.movieid)
        rows = self.get_data_from_commans(command)
        if rows:
            return True
        movie_count = 0
        try:
            sql = 'INSERT INTO movie_movie (movieid,title,year,length,genres,rate,poster,plot,trailer ) '
            sql+='VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'.format(movie.movieid,movie.title,movie.year,movie.length,movie.genres,movie.rate,movie.poster,movie.plot,movie.trailer)
            self.execute_sql(sql)
            rows = self.get_data_from_commans(command)
            return True
        except Exception as e:
            print('Movie Insert Failure: ' + movie.title, e)
            return False
    def add_actor(self,actor):
        command = 'SELECT * FROM movie_actor WHERE actorid = \'{0}\''.format(actor['actorid'])
        rows = self.get_data_from_commans(command)
        if rows:
            return
        sql = 'INSERT INTO movie_actor VALUES (\'{}\',\'{}\',\'{}\')'.format(actor['actorid'],actor['name'],actor['picurl'])
        try:
            self.execute_sql(sql)
        except Exception as e:
            print(actor['name'] + ' failure', e)
    def add_act(self,movie_id,actor_id):
        command = 'SELECT * FROM movie_act WHERE actorid_id = \'{0}\' AND  movieid_id = \'{1}\''.format(actor_id,movie_id)
        rows = self.get_data_from_commans(command)
        if rows:
            return
        sql = 'INSERT INTO movie_act(actorid_id, movieid_id) VALUES (\'{}\',\'{}\')'.format(actor_id,movie_id)
        try:
            self.execute_sql(sql)
        except Exception as e:
            print(movie_id + ' failure add actor '+actor_id, e)
    def get_all_old_movies_by_field(self,field):
        con = self.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute('SELECT '+str(field)+' FROM movie_movie')
        try:
            rows = cursorObj.fetchall()
            cursorObj.close()
            return rows
        except Exception as ex:
            print(ex)
        finally:
            con.close()
        return None
    def get_all_old_actors_by_field(self,field):
        con = self.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute('SELECT ' + field + ' FROM movie_actor')
        results = []
        try:
            rows = cursorObj.fetchall()
            cursorObj.close()
            for row in rows:
                s = str(row[0])
                results.append(s)
        except Exception as ex:
            print(ex)
        finally:
            con.close()
        return results
    def get_data_from_commans(self,command):
        con = self.sql_connection()
        cursorObj = con.cursor()

        try:
            cursorObj.execute(command)
            rows = cursorObj.fetchall()
            cursorObj.close()
            return rows
        except Exception as ex:
            print(ex)
            return None
        finally:
            con.close()


