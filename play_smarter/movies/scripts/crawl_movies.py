import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "play_smarter.settings")

from play_smarter.models import Movie


def crawl_movies():
    movie = Movie(douban_id=123, title='a title')

if __name__ == '__main__':
    crawl_movies()

