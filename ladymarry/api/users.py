from flask import Blueprint, abort, request
from flask_jwt import current_user, jwt_required
from werkzeug.datastructures import MultiDict

from ..forms import RegisterForm
from ..services import users
from . import route


bp = Blueprint('users', __name__, url_prefix='/users')


@route(bp, '/', methods=['POST'])
def register():
    data = MultiDict(dict(**request.json))
    form = RegisterForm(data, csrf_enabled=False)
    if form.validate():
        return users.register_user(email=form.email.data,
                                   password=form.password.data,
                                   first_name=form.first_name.data,
                                   last_name=form.last_name.data)
    else:
        # TODO: Log error here.
        abort(400)

@route(bp, '/me')
@jwt_required()
def me():
    if not current_user:
        abort(404)
    # We have to cast current_user to User class since SQLAlchemy model can't
    # be serialized to json.
    return users.user_from_model(current_user)

