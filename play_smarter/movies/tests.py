# -*- coding: utf-8 -*-
import os
import json

from django.test import TestCase

from .models import Movie, Genre
from django.db import IntegrityError
from .views import (
    _get_movies_raw,
    _get_or_create_movie_object,
    _parse_and_save_movie,
    _get_or_create_genre,
    _save_genres,
)



DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
douban_movie_search_response = open(os.path.join(
                                    DATA_DIR,
                                    'douban_movie_search_response.json')).read()
douban_movie_search_response = json.loads(douban_movie_search_response)


class MovieModelTests(TestCase):

    def test_save_without_id(self):
        movie = Movie(title='a title')
        with self.assertRaises(IntegrityError):
            movie.save()

    def test_attribute_can_be_saved(self):
        alt = 'www.example.com'

        movie = Movie(alt=alt, douban_id=123, title='a title')
        movie.save()

        self.assertEqual(alt, movie.alt)

    def test_save_genre(self):
        movie = Movie(douban_id=53)
        movie.save()

        genre_anime = Genre(name='动画')
        genre_anime.save()
        genre_love = Genre(name='爱情')
        genre_love.save()

        genre_anime.movie_set.add(movie)
        genre_anime.save()
        genre_love.movie_set.add(movie)
        genre_love.save()
        self.assertEqual(1, genre_anime.movie_set.count())
        self.assertEqual(1, genre_love.movie_set.count())


class MovieViewTests(TestCase):

    def test_get_movies_raw(self):
        movies = _get_movies_raw(douban_movie_search_response)

        self.assertEqual(20, len(movies))

    def test_get_or_create_movie_object(self):
        movie = _get_or_create_movie_object(53)

        self.assertIsNotNone(movie)

    def test_get_or_create_movie_object_already_exist(self):
        movie = Movie(douban_id=53, title='The Matrix')
        movie.save()

        movie = _get_or_create_movie_object(53)

        self.assertEqual('The Matrix', movie.title)

    def test_parse_and_save_movie(self):
        movies_raw = _get_movies_raw(douban_movie_search_response)
        movie_raw = movies_raw[0]

        _parse_and_save_movie(movie_raw)

        movie = Movie.objects.get(pk=4848115)
        self.assertEqual(179373, movie.collect_count)
        self.assertEqual(8.9, movie.rating_average)
        self.assertEqual(45, movie.rating_stars)
        self.assertEqual(2010, movie.year)
        self.assertEqual('http://img6.douban.com/view/movie_poster_cover/ipst/public/p709670262.jpg', movie.image_small)
        self.assertEqual("http://img6.douban.com/view/movie_poster_cover/lpst/public/p709670262.jpg", movie.image_large)
        self.assertEqual("http://img6.douban.com/view/movie_poster_cover/spst/public/p709670262.jpg", movie.image_medium)
        self.assertEqual("http://movie.douban.com/subject/4848115/", movie.alt)

    def test_get_or_create_genre(self):
        name = '动画'

        genre = _get_or_create_genre(name)

        self.assertEqual(name, genre.name)

    def test_get_or_create_genre_already_exist(self):
        name = '动画'
        genre = Genre(name=name)
        genre.save()

        genre = _get_or_create_genre(name)
        self.assertEqual(1, len(Genre.objects.all()))

    def test_save_genres(self):
        movie = Movie(douban_id=53)
        movie.save()
        genre_anime = Genre(name='动画')
        genre_anime.save()
        genre_love = Genre(name='爱情')
        genre_love.save()
        genres_name = [genre_anime.name, genre_love.name]

        _save_genres(movie, genres_name)

        self.assertEqual(1, genre_anime.movie_set.count())
        self.assertEqual(1, genre_love.movie_set.count())
        # genre_anime = _get_or_create_genre('动画')
        # genre_love = _get_or_create_genre('爱情')
        # self.assertEqual(1, genre_anime.movie_set.count())
        # self.assertEqual(1, genre_love.movie_set.count())
