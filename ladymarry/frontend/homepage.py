from flask import Blueprint, current_app

from . import route


bp = Blueprint('homepage', __name__)


@route(bp, '/')
def homepage():
    return current_app.send_static_file('wedding-checklist-fe/app/index.html')

@route(bp, '/img/<path:filename>')
def front_img(filename):
    """Serves static js, css, partial template files. """
    return current_app.send_static_file(
        'wedding-checklist-fe/src/img/' + filename)

@route(bp, '/<path:filename>')
def static(filename):
    """Serves static js, css, partial template files. """
    return current_app.send_static_file('wedding-checklist-fe/app/' + filename)

@route(bp, '/server/img/<path:filename>')
def send_file(filename):
    """Serves images from static folder.
    #TODO: Use Nginx static route instead of from Flask.
    """
    return current_app.send_static_file('static/' + filename)





