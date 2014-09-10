from functools import wraps

from flask import Response, jsonify, json, current_app, request

from .. import factory
from ..core import LadyMarryError, LadyMarryFormError, jwt
from ..helpers import JSONEncoder
from ..services import users as users_service


def create_app(settings_override=None):
    app = factory.create_app(__name__, __path__, settings_override)

    # Set the default JSON encoder.
    app.json_encoder = JSONEncoder

    # Register custom error handlers.
    app.errorhandler(LadyMarryError)(on_ladymarry_error)
    app.errorhandler(LadyMarryFormError)(on_ladymarry_form_error)
    app.errorhandler(404)(on_404)

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

# This has route /auth, see settings.py.
@jwt.authentication_handler
def authenticate(username, password):
    user = users_service.first(email=username)
    if not user:
        return None
    if not users_service.verify_password(user, password):
        return None

    return user

@jwt.user_handler
def load_user(payload):
    # This is a hack that actually put user_id into current_user.
    return payload['user_id']

# Error handlers.
def on_ladymarry_error(e):
    return jsonify(dict(error=e.message)), 400

def on_ladymarry_form_error(e):
    return jsonify(dict(error=e.get_message())), 400

def on_404(e):
    return jsonify(dict(error='Not found')), 404
    
