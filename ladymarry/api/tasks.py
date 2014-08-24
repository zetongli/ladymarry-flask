from dateutil import parser

from flask import Blueprint, abort, request

from ..services import tasks
from . import route


bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@route(bp, '/')
def get_all():
    """Returns all the tasks order by task_date and category. """
    model = tasks.__model__
    return model.query.order_by(model.task_date).order_by(model.category).all()

@route(bp, '/<task_id>')
def get_single(task_id):
    return tasks.get_or_404(task_id)

@route(bp, '/<task_id>', methods=['PUT'])
def update(task_id):
    # TODO: Verify params.
    return tasks.update(tasks.get_or_404(task_id), **request.json)

    

