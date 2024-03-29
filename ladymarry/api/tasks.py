from dateutil import parser

from flask import Blueprint, abort, request

from ..services import tasks
from . import route


task_bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@route(task_bp, '/')
def get_all_tasks():
    """Returns all the tasks order by task_date and category. """
    model = tasks.__model__
    return model.query.order_by(model.task_date).order_by(model.category).all()

@route(task_bp, '/<task_id>')
def get_single_task(task_id):
    return tasks.get_or_404(task_id)

@route(task_bp, '/<task_id>/related_tasks')
def get_related_tasks(task_id):
    task = tasks.get_or_404(task_id)
    return task.related_tasks.all()
