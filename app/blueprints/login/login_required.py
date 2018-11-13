from functools import wraps
from flask import session, abort
from config.settings import DevelopmentConfig


def login_required():
    def decorator(func):
        @wraps(func)
        def authorize(*args, **kwargs):
            if 'password' not in session or session['password'] != DevelopmentConfig.PASSWORD:
                abort(401)
            return func(*args, **kwargs)
        return authorize
    return decorator
