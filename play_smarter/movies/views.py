# -*- coding: utf-8 -*-
import requests

from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import loader

from .models import Movie, Genre


class IndexView(generic.ListView):
    template_name = 'movies/index.html'
    context_object_name = 'movies'

    def get_queryset(self):
        return Movie.objects.all()


# class DetailView(generic.DetailView):
#     model = Movie
#     template_name = 'movies/detail.html'

#     def get_queryset(self):
#         """
#         Excludes any questiosn that aren't published yet.
#         """
#         return Movie.objects.all()


# class ResultsView(generic.DetailView):
#     model = Movie
#     template_name = 'movies/results.html'

def crawl(request):
    if request.method == "POST":
        cartoons_url = _search_url_composer(tag=u'日本动画')
        response = requests.get(cartoons_url)
        _save_to_database(response)
    return render(request, 'movies/index.html', {'response': response.json()})
    # raise Exception(response)


def _search_url_composer(tag=None):
    base_url = 'http://api.douban.com/v2/movie/search?tag='
    return (base_url+tag)


def _save_to_database(response):
    data = response.json()
    movies_raw = _get_movies_raw(data)
    for movie_raw in movies_raw:
        _parse_and_save_movie(movie_raw)


def _get_movies_raw(data):
    return data['subjects']


def _parse_and_save_movie(movie_raw):
    douban_id = movie_raw['id']
    movie = _get_or_create_movie_object(douban_id)
    movie.title = movie_raw.pop('title', None)

    rating = movie_raw.pop('rating', {})
    movie.rating_average = rating.pop('average', None)
    movie.rating_stars = rating.pop('stars', None)

    movie.collect_count = movie_raw.pop('collect_count', None)
    movie.original_title = movie_raw.pop('original_title', None)
    movie.alt = movie_raw.pop('alt', None)
    movie.year = movie_raw.pop('year', None)

    images = movie_raw.pop('images', {})
    movie.image_small = images.pop('small', None)
    movie.image_medium = images.pop('medium', None)
    movie.image_large = images.pop('large', None)

    movie.save()

    genres_name = movie_raw.pop('genres', None)
    _save_genres(movie, genres_name)


def _get_or_create_movie_object(douban_id):
    douban_id = int(douban_id)
    try:
        movie = Movie.objects.get(pk=douban_id)
    except Movie.DoesNotExist:
        movie = Movie(douban_id=douban_id)
        movie.save()
    return movie

def _save_genres(movie, genres_name):
    for genre_name in genres_name:
        genre = _get_or_create_genre(genre_name)
        genre.movie_set.add(movie)
        genre.save()


def _get_or_create_genre(name):
    try:
        genre = Genre.objects.filter(name=name)[0]
    except IndexError:
        genre = Genre(name=name)
        genre.save()
    return genre
