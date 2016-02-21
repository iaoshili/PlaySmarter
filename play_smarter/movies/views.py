# -*- coding: utf-8 -*-
import requests

from bs4 import BeautifulSoup

from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import loader

from .models import Movie, Genre


COUNT_PER_PAGE = 20
MAX_PAGE_TO_CRAWL = 50


class IndexView(generic.ListView):
    template_name = 'movies/index.html'
    context_object_name = 'movies'

    def get_queryset(self):
        return sorted(Movie.objects.filter(watched__lte=False), key=lambda x: x.score, reverse=True)


def crawl(request):
    if request.method == "POST":
        tag = '日本动画'
        start = 0
        while start <= COUNT_PER_PAGE*MAX_PAGE_TO_CRAWL:
            cartoons_url = _search_url_composer(tag=tag, start=start)
            response = requests.get(cartoons_url)
            if _no_more_result(response):
                break
            else:
                _save_to_database(response)
                start += COUNT_PER_PAGE

    return render(request, 'movies/index.html', {'notification': response.json()})


def update_watched_movies(request):
    if request.method == "POST":
        base_url = 'http://movie.douban.com/people/49478062/collect?start='
        start = 0
        while True:
            response = requests.get(base_url+str(start))
            html_text = response.text
            if _should_continue(html_text):
                _save_movies_to_watched(html_text)
                start += 15
            else:
                break
    return render(request,
                  'movies/index.html',
                  {'notification': 'Watched movies updated'})


def _no_more_result(response):
    data = response.json()
    movies_raw = _get_movies_raw(data)
    if not movies_raw:
        return True


def _search_url_composer(tag=None, start=None):
    base_url = 'http://api.douban.com/v2/movie/search?tag='
    return ('{base_url}{tag}&start={start}').format(
                base_url=base_url,
                tag=tag,
                start=start)


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


def _should_continue(html_text):
    return ('nbg' in html_text)


def _save_movies_to_watched(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    for link in soup.find_all("a", "nbg"):
        url = str(link.get('href'))
        douban_id = url[32:-1]
        _update_watched_movie(douban_id)


def _update_watched_movie(douban_id):
    douban_id = int(douban_id)
    try:
        movie = Movie.objects.get(pk=douban_id)
        movie.watched = True
        movie.save()
    except Movie.DoesNotExist:
        pass
