from ..core import db
from ..helpers import JsonSerializer


class UserJsonSerializer(JsonSerializer):
    __json_hidden__ = ['password', 'tasks']

    def get_field_names(self):
        """Override base method as we need to return `token` field after
        registration.
        """
        for p in self.__mapper__.iterate_properties:
            yield p.key
        if hasattr(self, 'token'):
            yield 'token'


class WaitingUserJsonSerializer(JsonSerializer):
    pass


class User(UserJsonSerializer, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    wedding_date = db.Column(db.DateTime())
    registered_at = db.Column(db.DateTime())

    tasks = db.relationship('Task', backref='owner', lazy='dynamic')


# TODO: This is a temporary table for user waiting for invitation.
#       Remove this table once we don't need it any more.
class WaitingUser(WaitingUserJsonSerializer, db.Model):
    __tablename__ = 'waiting_users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    registered_at = db.Column(db.DateTime())



