import csv
import datetime

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
    """This command is used to init data, test user in db assuming
    db is empty.
    """
    def run(self):
        # Create scenarios.
        scenarios.init_scenarios()

        # Create test user.
        now = datetime.datetime.now()
        user = users.register_user(
            email='test@fotavo.com',
            password='123456',
            first_name='Alice',
            last_name='Wang',
            wedding_date=datetime.date(now.year + 1, now.month, now.day))
        schedulers.schedule_tasks(user)

        print 'Success!'

class RefreshDataCommand(Command):
    """This command is used to refresh content data while keeping existing
    users.
    NOTE: Right now all tasks will be refreshed for existing users.
    """
    def run(self):
        email = prompt('Enter email of user to be refreshed or \'all\' to ' +
                       'refresh for everyone. (Updating scenario for single ' +
                       'user is NOT supported.')
        if email == 'all':
            # Delete all tasks.
            for user in users.all():
                for task in user.tasks:
                    tasks.delete(task)

            # Delete all scenarios.
            for scenario in scenarios.all():
                scenarios.delete(scenario)

            # Create scenarios.
            scenarios.init_scenarios()

            # Refresh data for each user.
            for user in users.all():
                schedulers.schedule_tasks(user)
        else:
            u = users.first(email=email)
            if not u:
                print 'Invalid email.'
                return
            for task in u.tasks:
                tasks.delete(task)
            schedulers.schedule_tasks(u)

        print 'Success!'
        
            
