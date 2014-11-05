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
                       'refresh for everyone')
        task_file = prompt('Input customized task file (e.g. ' +
                           './ladymarry/data/export_task_data.csv ' +
                           'or press Enter space to use default data')
        task_file = (task_file if task_file.strip()
                     else current_app.config['TASK_DATA_FILE'])

        if email == 'all':
            # Delete all tasks.
            for user in users.all():
                for task in user.tasks:
                    tasks.delete(task)

            # Refresh data for each user.
            for user in users.all():
                schedulers.schedule_tasks(user, task_file=task_file)
        else:
            u = users.first(email=email)
            if not u:
                print 'Invalid email.'
                return
            for task in u.tasks:
                tasks.delete(task)
            schedulers.schedule_tasks(u, task_file=task_file)

        print 'Success!'

class ExportDataCommand(Command):
    def run(self):
        email = prompt('Email of the exported user')
        u = users.first(email=email)
        if not u:
            print 'Invalid email.'
            return
        schedulers.export_tasks(u, current_app.config['DEFAULT_EXPORT_FILE'])

        print 'Success!'
        
            
