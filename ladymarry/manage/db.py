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
        with open('./ladymarry/data/data.csv', 'r') as f:
            reader = csv.reader(f)
            num = 0
            for row in reader:
                if num > 0:
                    task = tasks.create(
                        category=row[0],
                        title=row[1],
                        task_date=row[2],
                        description=row[3],
                        tutorial=row[4],
                        resource=row[5],
                        image=row[7])
                num += 1

            # Set up related tasks.
            f.seek(0)
            k = 0
            for row in reader:
                if k > 0 and row[6]:
                    related_task_rows = row[6].split(',')
                    task = tasks.get(k)
                    for r in related_task_rows:
                        task.related_tasks.append(tasks.get(int(r.strip()) - 1))
                    tasks.save(task)
                k += 1


            #################################
            # This is used for testing scenarios.
            scenario1 = scenarios.create(title='scenario1',
                                         when='mornint',
                                         description='blabla')
            scenario2 = scenarios.create(title='scenario2',
                                         when='morninggggggn',
                                         description='blablabbbbb')

            task1 = tasks.get(1)
            task2 = tasks.get(2)
            task3 = tasks.get(3)

            task1.scenarios.append(scenario1)
            task1.scenarios.append(scenario2)
            tasks.save(task1)

            task2.scenarios.append(scenario1)
            task2.scenarios.append(scenario2)
            tasks.save(task2)

            task3.scenarios.append(scenario1)
            tasks.save(task3)
            #################################            
            
            
            print 'Created %d tasks successfully.' % num
