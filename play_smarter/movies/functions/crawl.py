import requests

from movies.models import Movie, Genre

COUNT_PER_PAGE = 20
MAX_PAGE_TO_CRAWL = 50


def crawl_by_tag(tag):
    start = 0
    while start <= COUNT_PER_PAGE*MAX_PAGE_TO_CRAWL:
        movies_url = _search_url_composer(tag=tag, start=start)
        response = requests.get(movies_url)
        if _no_more_result(response):
            break
        else:
            parse_and_save_movies(response)
            start += COUNT_PER_PAGE

        return response


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


def _get_movies_raw(data):
    return data['subjects']


def parse_and_save_movies(response):
    data = response.json()
    movies_raw = _get_movies_raw(data)
    for movie_raw in movies_raw:
        _parse_and_save_movie(movie_raw)


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
