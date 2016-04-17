import requests

from bs4 import BeautifulSoup

from movies.models import Movie
from movies.errors.errors import InvalidInput


def _update_watched_movies():
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


def _should_continue(html_text):
    return ('nbg' in html_text)


def _save_movies_to_watched(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    for link in soup.find_all("a", "nbg"):
        href = str(link.get('href'))
        douban_id = get_id_from_href(href)
        _update_watched_movie(douban_id)


def _update_watched_movie(douban_id):
    douban_id = int(douban_id)
    try:
        movie = Movie.objects.get(pk=douban_id)
        movie.watched = True
        movie.save()
    except Movie.DoesNotExist:
        pass


def get_id_from_href(href):
    num = [int(s) for s in href.split('/') if s.isdigit()]
    if len(num) != 1:
        raise InvalidInput(message='invalid href, your href is: %s' % href)
    return num[0]
