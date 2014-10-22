from flask import json
from flask.ext.script import Command, prompt

from ..services import tasks


class CreateTaskCommand(Command):
    def run(self):
        title = prompt('title')
        category = prompt('category in number')
        task_date = prompt('task_date')

        new_task = tasks.create(
            title=title, category=category, task_date=task_date)
        print 'Task created.'


class ListTaskCommand(Command):
    def run(self):
        for task in tasks.all():
            print '\n%s' % json.dumps(task, indent=2)


class DeleteTaskCommand(Command):
    def run(self):
        id = prompt('id')
        task = tasks.first(id=id)
        if not task:
            print 'Invalid task id.'
        else:
            tasks.delete(task)
            print 'Task deleted successfully.'

            


