from flask import json
from flask.ext.script import Command, prompt

from ..models import Task
from ..services import tasks, users, waiting_users


class ListUserCommand(Command):
    def run(self):
        for u in users.all():
            print 'email: %s \t registered_at: %s' % (u.email, u.registered_at)


class DeleteUserCommand(Command):
    def run(self):
        email = prompt('email')
        u = users.first(email=email)
        if not u:
            print 'Invalid email.'
        else:
            users.delete(u)
            print 'Delete successfully.'


class GetTaskForUserCommand(Command):
    def run(self):
        email = prompt('User email')
        u = users.first(email=email)
        if not u:
            print 'Invalid email.'
            return
        
        title = prompt('Task title')
        task = u.tasks.filter_by(title=title).first()
        if not task:
            print 'Cannot find task with title: %s' % title
            return
        print json.dumps(task, indent=2)


class UpdateTaskForUserCommand(Command):
    def run(self):
        email = prompt('User email')
        u = users.first(email=email)
        if not u:
            print 'Invalid email.'
            return
        
        title = prompt('Task title')
        task = u.tasks.filter_by(title=title).first()
        if not task:
            print 'Cannot find task with title: %s' % title
            return

        field = prompt('Update field name')
        value = prompt('Update field value')
        task = tasks.update(task, **{field: value})
        print json.dumps(task, indent=2)

        
class DeleteTaskForUserCommand(Command):
    def run(self):
        email = prompt('User email')
        u = users.first(email=email)
        if not u:
            print 'Invalid email.'
            return
        
        title = prompt('Task title')
        task = u.tasks.filter_by(title=title).first()
        if not task:
            print 'Cannot find task with title: %s' % title
            return
        tasks.delete(task)
        print 'Success'
            

class ListWaitingUserCommand(Command):
    def run(self):
        for u in waiting_users.all():
            print 'email: %s \t registered_at: %s' % (u.email, u.registered_at)


class DeleteWaitingUserCommand(Command):
    def run(self):
        email = prompt('email')
        u = waiting_users.first(email=email)
        if not u:
            print 'Invalid email.'
        else:
            waiting_users.delete(u)
            print 'Delete successfully.'
