# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from django.test import TestCase

from movies.functions.update_watched_movies import (_save_movies_to_watched,
                                                    get_id_from_href)
from movies.errors.errors import InvalidInput
from movies.models import Movie

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
douban_watched_movies = open(os.path.join(DATA_DIR, 'douban_watched_movies')).read()


class TestUpdateWatchedMovies(TestCase):

    def test_save_movies_to_watched(self):
        watched_movie = Movie(douban_id=1421721)
        watched_movie.save()
        _save_movies_to_watched(douban_watched_movies)

        movies = Movie.objects.all()

        self.assertEquals(len(movies), 1)

    def test_get_id_from_href(self):
        href = "http://movie.douban.com/subject/1421721/"

        douban_id = get_id_from_href(href)

        self.assertEquals(douban_id, 1421721)

    def test_get_id_from_href_exception(self):
        href = '525/323'

        with self.assertRaises(InvalidInput):
            douban_id = get_id_from_href(href)
