from flask import Blueprint, abort, request

from . import route


bp = Blueprint('static', __name__, url_prefix='/static')


@route(bp, '/<path:filename>')
def send_file(filename):
    return send_from_directory('./ladymarry/frontend/static', filename)
