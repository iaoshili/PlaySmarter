# -*- coding: utf-8 -*-
from django.shortcuts import render

from functions.set_status import _get_boolean_from_ajax, _set_status
from functions.crawl import crawl_by_tag
from functions.update_watched_movies import _update_watched_movies

from .models import Movie, Genre


FIND_SERIES = True
BASE_RATING = 7.6


def index(request):
    movies = sorted(Movie.objects.filter(watched=False,
                                         boring=False,
                                         series=FIND_SERIES,
                                         rating_average__gte=BASE_RATING), key=lambda x: x.score, reverse=True)
    genres = Genre.objects.all()
    context = {'movies': movies, 'genres': genres}
    return render(request, 'movies/index.html', context)


def filter(request):
    if request.method == "GET":
        genre = Genre.objects.get(pk=int(request.GET['genre']))
        genres = Genre.objects.all()
        movie_genre = genre.movie_set.all()
        movies = sorted(movie_genre.filter(watched=False,
                                           boring=False,
                                           series=FIND_SERIES,
                                           rating_average__gte=BASE_RATING), key=lambda x: x.score, reverse=True)
        context = {'movies': movies, 'genres': genres}
        return render(request, 'movies/index.html', context)


def set_status(request):
    if request.method == "POST":
        movie_id = request.POST.get('movie_id')
        boring = _get_boolean_from_ajax(request.POST.get('boring'))
        watched = _get_boolean_from_ajax(request.POST.get('watched'))
        series = _get_boolean_from_ajax(request.POST.get('series'))
        movie = Movie.objects.get(pk=movie_id)
        _set_status(movie,
                    boring=boring,
                    watched=watched,
                    series=series)
    return render(request, 'movies/index.html', {'notification': 'fuck yeah'})


def crawl(request):
    if request.method == "POST":
        response = crawl_by_tag('香港')

    return render(request, 'movies/index.html', {'notification': response.json()})


def update_watched_movies(request):
    if request.method == "POST":
        _update_watched_movies()
    return render(request,
                  'movies/index.html',
                  {'notification': 'Watched movies updated'})


# def _no_more_result(response):
#     data = response.json()
#     movies_raw = _get_movies_raw(data)
#     if not movies_raw:
#         return True


# def _search_url_composer(tag=None, start=None):
#     base_url = 'http://api.douban.com/v2/movie/search?tag='
#     return ('{base_url}{tag}&start={start}').format(
#                 base_url=base_url,
#                 tag=tag,
#                 start=start)


# def parse_and_save_movies(response):
#     data = response.json()
#     movies_raw = _get_movies_raw(data)
#     for movie_raw in movies_raw:
#         _parse_and_save_movie(movie_raw)


# def _get_movies_raw(data):
#     return data['subjects']


# def _parse_and_save_movie(movie_raw):
#     douban_id = movie_raw['id']
#     movie = _get_or_create_movie_object(douban_id)
#     movie.title = movie_raw.pop('title', None)

#     rating = movie_raw.pop('rating', {})
#     movie.rating_average = rating.pop('average', None)
#     movie.rating_stars = rating.pop('stars', None)

#     movie.collect_count = movie_raw.pop('collect_count', None)
#     movie.original_title = movie_raw.pop('original_title', None)
#     movie.alt = movie_raw.pop('alt', None)
#     movie.year = movie_raw.pop('year', None)

#     images = movie_raw.pop('images', {})
#     movie.image_small = images.pop('small', None)
#     movie.image_medium = images.pop('medium', None)
#     movie.image_large = images.pop('large', None)

#     movie.save()

#     genres_name = movie_raw.pop('genres', None)
#     _save_genres(movie, genres_name)


# def _get_or_create_movie_object(douban_id):
#     douban_id = int(douban_id)
#     try:
#         movie = Movie.objects.get(pk=douban_id)
#     except Movie.DoesNotExist:
#         movie = Movie(douban_id=douban_id)
#         movie.save()
#     return movie


# def _save_genres(movie, genres_name):
#     for genre_name in genres_name:
#         genre = _get_or_create_genre(genre_name)
#         genre.movie_set.add(movie)
#         genre.save()


# def _get_or_create_genre(name):
#     try:
#         genre = Genre.objects.filter(name=name)[0]
#     except IndexError:
#         genre = Genre(name=name)
#         genre.save()
#     return genre









