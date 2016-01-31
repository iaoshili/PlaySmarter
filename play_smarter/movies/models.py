from __future__ import unicode_literals

from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)  # Chinese title
    rating_average = models.FloatField(null=True, blank=True)  # average score in the scope of 10
    rating_stars = models.SmallIntegerField(null=True, blank=True)  # stars in the scope of 100?
    collect_count = models.IntegerField(null=True, blank=True)  # Num of people who viewed the movie
    original_title = models.CharField(max_length=200, null=True, blank=True)  # English title
    alt = models.URLField(null=True, blank=True)  # The URL of this movie
    douban_id = models.PositiveIntegerField(primary_key=True)
    year = models.SmallIntegerField(null=True, blank=True)
    image_small = models.URLField(null=True, blank=True)
    image_medium = models.URLField(null=True, blank=True)
    image_large = models.URLField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)  # Detail view
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def score(self):
        if self.collect_count and self.rating_average:
            return self.collect_count*self.rating_average
        else:
            return 0

    def __str__(self):
        return self.title
