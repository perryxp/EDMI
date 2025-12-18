from functools import wraps
from flask import request, current_app

def requireApikey(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):
        security = current_app.container.get('securityService')
        security.authorize(request)
        return fn(*args, **kwargs)

    return wrapper
