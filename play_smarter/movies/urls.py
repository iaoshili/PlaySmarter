from django.conf.urls import url

from . import views


app_name = 'movies'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^/crawl/$', views.crawl, name='crawl'),
]
