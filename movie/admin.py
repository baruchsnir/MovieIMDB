from django.contrib import admin

# Register your models here.

from .models import Movie,Actor,Review

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'movieid', 'rate')


class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'actorid')


admin.site.register(Movie, MovieAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Review)

