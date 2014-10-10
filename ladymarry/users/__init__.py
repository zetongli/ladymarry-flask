from datetime import datetime
from passlib.apps import custom_app_context as pwd_context

from flask_jwt import current_user

from ..core import Service
from .models import User, WaitingUser


class UsersService(Service):
    __model__ = User

    def current_user(self):
        """IMPORTANT: This method should only be used within @jwt_required
        decorator.
        Returns the current user model.
        """
        return self.get(current_user)

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


class WaitingUsersService(Service):
    __model__ = WaitingUser
