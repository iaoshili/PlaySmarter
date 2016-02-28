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
    _search_url_composer,
    _should_continue,
    _save_movies_to_watched,
    _update_watched_movie,
    _set_status,
)


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
douban_movie_search_response = open(os.path.join(
                                    DATA_DIR,
                                    'douban_movie_search_response.json')).read()
douban_movie_search_response = json.loads(douban_movie_search_response)
douban_watched_movies = open(os.path.join(DATA_DIR, 'douban_watched_movies')).read()


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

    def test_set_watched_true(self):
        movie = Movie(douban_id=1)
        movie.save()
        self.assertFalse(movie.watched)

        movie.watched = True
        movie.save()
        self.assertTrue(movie.watched)


class MovieViewTests(TestCase):

    def setUp(self):
        self.movie = Movie.objects.create(douban_id=2046)

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

    def test_search_url_composer(self):
        tag = '动画'
        start = 20

        url = _search_url_composer(tag=tag, start=start)
        self.assertEqual('http://api.douban.com/v2/movie/search?tag=动画&start=20', url)

    def test_update_watched_movie(self):
        movie_not_watched = Movie(douban_id=1)
        movie_not_watched.save()
        movie_to_be_watched = Movie(douban_id=55)
        movie_to_be_watched.save()

        _update_watched_movie(55)

        movie_to_be_watched = Movie.objects.get(pk=55)
        self.assertTrue(movie_to_be_watched.watched)
        self.assertFalse(movie_not_watched.watched)

    def test_save_movies_to_watched(self):
        movie_not_watched = Movie(douban_id=1)
        movie_not_watched.save()
        movie_1 = Movie(douban_id=1421721)
        movie_1.save()
        movie_2 = Movie(douban_id=10563743)
        movie_2.save()
        _save_movies_to_watched(douban_watched_movies)

        movie_1 = Movie.objects.get(pk=1421721)
        movie_2 = Movie.objects.get(pk=10563743)
        movie_not_watched = Movie.objects.get(pk=movie_not_watched.douban_id)
        self.assertTrue(movie_1.watched)
        self.assertTrue(movie_2.watched)
        self.assertFalse(movie_not_watched.watched)

    def test_should_continue(self):
        should_continue = _should_continue(douban_watched_movies)

        self.assertTrue(should_continue)

    def test_should_continue_should_really_stop(self):
        html_text = 'text_without_feature_word_in_it'

        should_continue = _should_continue(html_text)

        self.assertFalse(should_continue)

    def test_set_status_false(self):
        boring = False

        _set_status(self.movie, boring=boring)

        movie_updated = Movie.objects.get(pk=self.movie.douban_id)
        self.assertFalse(movie_updated.boring)
