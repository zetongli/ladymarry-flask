from functools import wraps

from flask import Response, jsonify, json, current_app, request

from ..helpers import JSONEncoder
from .. import factory


def create_app(settings_override=None):
    app = factory.create_app(__name__, __path__, settings_override)

    # Set the default JSON encoder
    app.json_encoder = JSONEncoder

    return app


def route(bp, *args, **kwargs):
    kwargs.setdefault('strict_slashes', False)

    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            sc = 200
            rv = f(*args, **kwargs)
            if isinstance(rv, tuple):
                sc = rv[1]
                rv = rv[0]

            indent = None
            if (current_app.config['JSONIFY_PRETTYPRINT_REGULAR']
                and not request.is_xhr):
                indent = 2
            return current_app.response_class(json.dumps(rv, indent=indent),
                                              mimetype='application/json')
        return f

    return decorator
