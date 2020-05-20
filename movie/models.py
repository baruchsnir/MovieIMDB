from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Movie(models.Model):
    movieid = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=30)
    year = models.CharField(max_length=4)
    length = models.CharField(max_length=10)
    genres = models.CharField(max_length=100)
    rate = models.IntegerField(default=0)
    poster = models.URLField(default='')
    plot = models.CharField(max_length=500)
    trailer = models.URLField(default='')

    def __str__(self):
        return self.movieid + '|' + self.title

    @staticmethod
    def get_name():
        return 'movie'


class Actor(models.Model):
    actorid = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=30)
    photo = models.URLField()

    def __str__(self):
        return self.actorid + '|' + self.name

    @staticmethod
    def get_name():
        return 'actor'

class Popularity(models.Model):
    movieid = models.ForeignKey('Movie', default=' ', on_delete=models.CASCADE)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.movieid.movieid + '|' + str(self.weight)
class Act(models.Model):
    movieid = models.ForeignKey('Movie', default=1, on_delete=models.CASCADE)
    actorid = models.ForeignKey('Actor', default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.actorid.actorid + '|' + self.movieid.movieid
class Expect(models.Model):
    username = models.CharField(max_length=150)
    movieid = models.ForeignKey('Movie', default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.username + '|' + self.movieid.movieid
class Seen(models.Model):
    username = models.CharField(max_length=150)
    movieid = models.ForeignKey('Movie', default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.username + '|' + self.movieid.movieid
class Review(models.Model):
    movieid = models.TextField()
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(
        default=1, validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.movieid) + '|' + self.comment

    def __unicode__(self):
        return str(self.movieid) + '|' + self.comment

    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)

    def my_save(self):
        self.save()

