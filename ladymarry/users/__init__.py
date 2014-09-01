from datetime import datetime
from passlib.apps import custom_app_context as pwd_context

from flask_jwt import current_user

from ..core import Service
from .models import User


class UsersService(Service):
    __model__ = User

    def current_user(self):
        """IMPORTANT: This method should only be used within @jwt_required
        decorator.
        """
        assert current_user
        # We have to cast current_user to User class since SQLAlchemy model
        # can't be serialized to json.
        return self._user_from_model(current_user)

    def register_user(self, **kwargs):
        """This method should be called after RegisterForm validation. """
        password = kwargs.get('password', None)
        assert password
        kwargs['password'] = self.hash_password(password)
        kwargs.pop('confirm_passoword', None)
        
        if 'registered_at' not in kwargs:
            kwargs['registered_at'] = datetime.now()

        return self.create(**kwargs)

    def hash_password(self, password):
        return pwd_context.encrypt(password)

    def verify_password(self, user, password):
        return pwd_context.verify(password, user.password)

    def _user_from_model(self, sqlalchemy_user):
        """Returns a User object from SQLAlchemy User model. """
        d = {k.key: getattr(sqlalchemy_user, k.key)
             for k in sqlalchemy_user.__mapper__.iterate_properties}
        return self.new(**d)
