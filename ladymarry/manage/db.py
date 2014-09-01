import csv

from flask import current_app
from flask.ext.script import Command, prompt, prompt_pass

from ..core import db
from ..models import *
from ..services import *


class CreateDBCommand(Command):
    def run(self):
        db.create_all()


class DropDBCommand(Command):
    def run(self):
        db.drop_all()


class ClearDBCommand(Command):
    def run(self):
        db.drop_all()
        db.create_all()


class SeedDBCommand(Command):
    def run(self):
        # Create scenarios.
        # TODO: Use real data.
        scenario1 = scenarios.create(title='scenario1',
                                     when='mornint',
                                     description='blabla')
        scenario2 = scenarios.create(title='scenario2',
                                     when='morninggggggn',
                                     description='blablabbbbb')

        # Create test user.
        user = users.register_user(email='test@fotavo.com',
                                   password='123456',
                                   first_name='Alice',
                                   last_name='Wang')
        tasks.init_tasks_for_user(user)

        print 'Success!'
