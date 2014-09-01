from flask import Blueprint, abort, request
from flask_jwt import jwt_required
from werkzeug.datastructures import MultiDict

from ..forms import RegisterForm
from ..models import Scenario, Task
from ..services import *
from . import route


bp = Blueprint('users', __name__, url_prefix='/users')


@route(bp, '/', methods=['POST'])
def register():
    data = MultiDict(dict(**request.json))
    form = RegisterForm(data, csrf_enabled=False)
    if form.validate():
        user = users.register_user(email=form.email.data,
                                   password=form.password.data,
                                   first_name=form.first_name.data,
                                   last_name=form.last_name.data)
        tasks.init_tasks_for_user(user)
        return user
    else:
        # TODO: Log error here.
        abort(400)

@route(bp, '/me')
@jwt_required()
def me():
    return users.current_user()

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
