from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import render
from . import views
#this is for calling url of html file from different application
#then we have to call the refference as    <h1><a href="{% url 'list' %}"><img width="100" height="100" src="{% static '/images/baruch.jpg' %}"></a></h1>
#as    <h1><a href="{% url 'articles.list' %}"><img width="100" height="100" src="{% static '/images/baruch.jpg' %}"></a></h1>
urlpatterns = [
    path('admin/', admin.site.urls),
    path('movie/', include('movie.urls')),
    path('accounts/', include('accounts.urls')),
    path("", views.index, name="index"),
    path('.*',lambda request: render(request, '404.html'), name='404'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)