from flask import Blueprint, current_app, render_template

from . import route


bp = Blueprint('homepage', __name__)


@route(bp, '/')
def homepage():
    return render_template('index.html')

@route(bp, '/<path:filename>')
def static(filename):
    """Serves static js, css, partial template files. """
    return current_app.send_static_file('app/' + filename)
