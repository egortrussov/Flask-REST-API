from . import auth_middleware

from flask import request

def token_required(route_function):
    """
    Validates token before accesing a route 
    """
    def wrapper(*args):
        decoded_token = None if 'token' not in request.headers.keys(lower=True) else auth_middleware.decode_token(request.headers['token'])
        if not decoded_token:
            return { 'error': 'Invalid token' }, 400
        return route_function(decoded_token)
    wrapper.__name__ = route_function.__name__
    return wrapper

