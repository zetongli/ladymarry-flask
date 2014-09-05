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
