from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import unittest
import HtmlTestRunner
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas

#pip install webdriver_manager
#to install pip install html-testRunner
#pip install beautifulsoup4
#pip freeze
#pip list
class moviedata():
    movieid = ''
    title = ''
    year = ''
    length = ''
    genres =  ''
    rate = 0
    poster = ''
    plot = ''
    trailer = ''
    actors = ''
class MngIMDB(unittest.TestCase):
    movie_list = []
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        cls.driver.implicitly_wait(2)
        cls.driver.maximize_window()
        cls.url = "https://www.imdb.com//"

    def search_actor(self,name):
        results = {'name':name}
        self.driver.get(self.url)
        self.driver.find_element_by_name("q").clear()
        self.driver.find_element_by_name("q").send_keys(name + Keys.RETURN)
        time.sleep(2)
        soup = BeautifulSoup(self.driver.page_source)
        sections = soup.find_all('div', attrs={'class':'findSection'})
        for sec in sections:
            text = sec.text
            if str(name).lower() in str(text).lower() and 'Names' in text:
                links = sec.find_all('a')
                for link in links:
                    if str(name).lower() in str(link.text).lower():
                        fullLink = link.get('href')
                        data = str(fullLink).split('/')
                        actorid = data[2]
                        results['actorid'] = actorid
                        results = self.get_user_picture(results,fullLink)
                        return results


        # Find the value of org?
        # val = org.get_attribute("attribute name")
    def get_user_picture(self,results,link):
        self.driver.get(self.url+ link)
        time.sleep(2)
        org = self.driver.find_element_by_id('name-poster')
        val = org.get_attribute("src")
        print('picture url',val)
        results['picurl'] = val
        return results

    def search_movie(self,name):
        results = {'name':name}
        self.driver.get(self.url)
        self.driver.find_element_by_name("q").clear()
        self.driver.find_element_by_name("q").send_keys(name + Keys.RETURN)
        time.sleep(2)
        soup = BeautifulSoup(self.driver.page_source)
        sections = soup.find_all('div', attrs={'class':'findSection'})
        for sec in sections:
            text = sec.text
            if str(name).lower() in str(text).lower() and 'Titles' in text:
                links = sec.find_all('a')
                for link in links:
                    if str(name).lower() in str(link.text).lower():
                        fullLink = link.get('href')
                        data = str(fullLink).split('/')
                        movieid = data[2]
                        results['movieid'] = movieid
                        results = self.get_movie_picture(results,fullLink)
                        results = self.get_movie_Trailer(results)
                        results = self.get_movie_rateing(results)
                        print('results',results)
                        return results

    def get_movie_picture(self,results,link):
        self.driver.get(self.url+ link)
        time.sleep(2)
        poster = self.driver.find_element_by_class_name('poster')
        img = poster.find_element_by_tag_name('img')
        val = img.get_attribute("src")
        print('picture url',val)
        results['picurl'] = val
        return results
    def get_movie_Trailer(self,results):
        try:
            div = self.driver.find_element_by_class_name('slate')
            a = div.find_element_by_tag_name('a')
            val = a.get_attribute("href")
            print('Trailer',val)
            results['trailer'] = val
        except:
            results['trailer'] = ''
        return results

    def get_movie_rateing(self, results):
        try:
            div = self.driver.find_element_by_class_name('ratings_wrapper')
            spans = div.find_elements_by_tag_name('span')
            for span in spans:
                val = span.get_attribute("itemprop")
                if  val == 'ratingValue':
                    rate = span.text
                    print('rate', rate)
                    results['rate'] = rate
                    break
        except:
            results['rate'] = ''
        return results


    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()
        print("Test Completed")
    def load_data_from_csv(self):
        df = pandas.read_csv('c:\\temp\\netflix_titles.csv', index_col='show_id',
            parse_dates=['release_year'],
            header=0,
            names=['show_id','type','title','director','cast','country','date_added','release_year','rating','duration','listed_in','description'])
        for i, j in df.iterrows():
            type = j['type']
            if type == 'Movie':
                movie = moviedata()
                movie.movieid = i
                movie.title = j['title']
                movie.actors = j['cast']
                movie.year = j['release_year']
                s = str(j['duration'].replace(' min', ''))
                movie.length = s.strip()
                movie.plot = j['description']
                movie.genres = j['listed_in']
                movie.rate = ''
                movie.trailer = ''
                movie.poster = ''
                self.movie_list.append(movie)
        return self.movie_list
