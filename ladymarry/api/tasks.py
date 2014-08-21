from dateutil import parser

from flask import Blueprint, abort, request

from ..services import tasks
from . import route


bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')


@route(bp, '/')
def get_all():
    since = request.args.get('since', None)
    to = request.args.get('to', None)

    return tasks.find_between_date(since, to)

@route(bp, '/<task_id>')
def get_single(task_id):
    return tasks.get_or_404(task_id)

@route(bp, '/<task_id>', methods=['PUT'])
def update(task_id):
    # TODO: Verify params.
    return tasks.update(tasks.get_or_404(task_id), **request.json)

    

