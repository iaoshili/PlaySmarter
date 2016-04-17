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
