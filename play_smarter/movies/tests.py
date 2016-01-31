from django.test import TestCase

from .models import Movie, Genre
from django.db import IntegrityError

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
