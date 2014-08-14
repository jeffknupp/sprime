"""Decorators for sandman convenience functions."""

import functools
import hashlib
from flask import jsonify, request, make_response


def cache_control(*directives):
    """Add Cache-Control directives to the response headers.

    :param list directives: Cache-Control directives to add
    """
    def decorator(func):
        """The actual decorator function."""
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            """Call the view function and add the Cache-Control directives to
            the response."""
            response = func(*args, **kwargs)
            response = make_response(response)
            response.headers['Cache-Control'] = ', '.join(directives)
            return response
        return wrapped
    return decorator


def no_cache(func):
    """A decorator to mark that a view function's response should not be
    cached.

    :param func: view function
    """
    return cache_control('no-cache', 'no-store', 'max-age=0')(func)


def etag(func):
    """Return a decorator that generates proper ETag values for a response.

    :param func: view function
    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        """Call the view function and generate an ETag value, checking the
        headers to determine what response to send."""
        # only for HEAD and GET requests
        assert request.method in ['HEAD', 'GET'],\
            '@etag is only supported for GET requests'
        response = func(*args, **kwargs)
        response = make_response(response)
        etag_value = '"' + hashlib.md5(response.get_data()).hexdigest() + '"'
        response.headers['ETag'] = etag_value
        if_match = request.headers.get('If-Match')
        if_none_match = request.headers.get('If-None-Match')
        if if_match:
            etag_list = [tag.strip() for tag in if_match.split(',')]
            if etag_value not in etag_list and '*' not in etag_list:
                response = precondition_failed()
        elif if_none_match:
            etag_list = [tag.strip() for tag in if_none_match.split(',')]
            if etag_value in etag_list or '*' in etag_list:
                response = not_modified()
        return response
    return wrapped


def not_modified():
    """Return an HTTP 304 response if the resource hasn't been modified based
    on the ETag value."""
    response = jsonify({'status': 304, 'error': 'not modified'})
    response.status_code = 304
    return response


def precondition_failed():
    """Return an HTTP 412 if no ETags match on an If-Match."""
    response = jsonify({'status': 412, 'error': 'precondition failed'})
    response.status_code = 412
    return response
