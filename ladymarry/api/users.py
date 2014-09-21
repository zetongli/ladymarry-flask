import logging

from flask import Blueprint, abort, request
from flask_jwt import generate_token, jwt_required
from werkzeug.datastructures import MultiDict

from ..core import LadyMarryError, LadyMarryFormError
from ..forms import RegisterForm, UpdateForm
from ..models import Scenario, Task
from ..services import tasks, users
from . import route

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)

bp = Blueprint('users', __name__, url_prefix='/users')


# Auth APIs.
@route(bp, '/', methods=['POST'])
def register():
    """Returns the registered user with token if success. """
    data = MultiDict(dict(**request.json))
    form = RegisterForm(data, csrf_enabled=False)
    if form.validate():
        # Check if email is used.
        if users.first(email=form.email.data):
            raise LadyMarryError(
                'Email %s is already registered.' % form.email.data)
        user = users.register_user(email=form.email.data,
                                   password=form.password.data,
                                   first_name=form.first_name.data,
                                   last_name=form.last_name.data,
                                   wedding_date=form.wedding_date.data)
        if form.wedding_date.data:
            tasks.schedule_tasks_for_user(user)

        # Generate JWT token for this user.
        user.token = generate_token(user)
        return user
    else:
        logger.info('Register fail: %s', form.errors)
        raise LadyMarryFormError(form.errors)

@route(bp, '/me')
@jwt_required()
def me():
    return users.current_user()

@route(bp, '/me', methods=['PUT'])
@jwt_required()
def update():
    data = MultiDict(dict(**request.json))
    form = UpdateForm(data, csrf_enabled=False)
    if form.validate():
        user = users.update(users.current_user(), **request.json)

        # Re-schedule tasks if wedding_date is updated.
        if form.wedding_date.data:
            tasks.schedule_tasks_for_user(user)
        return user
    else:
        logger.info('Update fail: %s', form.errors)
        raise LadyMarryFormError(form.errors)

# Tasks APIs.
@route(bp, '/me/tasks')
@jwt_required()
def get_tasks_for_user():
    scenario_id = request.args.get('scenario_id', None)
    if not scenario_id:
        return users.current_user().tasks.order_by(
            Task.task_date, Task.category).all()
    else:
        return users.current_user().tasks.filter(
            Task.scenarios.any(Scenario.id==scenario_id)).order_by(
                Task.task_date, Task.category).all()

@route(bp, '/me/tasks', methods=['POST'])
@jwt_required()
def create_tasks_for_user():
    # TODO: Supports scenarios.
    params = request.json
    if 'owner_id' in params and params['owner_id'] != users.current_user().id:
        raise LadyMarryError('Cannot create task for other users.')
    params['owner_id'] = users.current_user().id
    return tasks.create(**params)


# Single task APIs.
@route(bp, '/me/tasks/<task_id>')
@jwt_required()
def get_single_task(task_id):
    return tasks.get_or_404(task_id)

@route(bp, '/me/tasks/<task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    # TODO: Verify params.
    return tasks.update(tasks.get_or_404(task_id), **request.json)

# Related tasks APIs.
@route(bp, '/me/tasks/<task_id>/related_tasks')
@jwt_required()
def get_related_tasks(task_id):
    task = tasks.get_or_404(task_id)
    return task.related_tasks.all()

