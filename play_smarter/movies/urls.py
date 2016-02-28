from django.conf.urls import url

from . import views


app_name = 'movies'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^/crawl/$', views.crawl, name='crawl'),
    url(r'^/update_watched_movies/$',
        views.update_watched_movies,
        name='update_watched_movies'),
    url(r'^/filter/$', views.filter, name='filter'),
    url(r'^set_status/$', views.set_status, name='set_status'),
]
