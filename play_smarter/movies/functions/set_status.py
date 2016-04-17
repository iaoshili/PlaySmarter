def _get_boolean_from_ajax(value):
    if value == 'true':
        return True
    elif value == 'false':
        return False
    else:
        return None


def _set_status(movie,
                boring=None,
                watched=None,
                series=None):
    if boring is not None:
        movie.boring = boring
    if watched is not None:
        movie.watched = watched
    if series is not None:
        movie.series = series
    movie.save()
