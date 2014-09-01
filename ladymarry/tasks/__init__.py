import csv
from dateutil import parser

from flask import abort, current_app

from ..core import Service
from .models import Scenario, Task, TaskStatus, TaskCategory


class ScenariosService(Service):
    __model__ = Scenario


class TasksService(Service):
    __model__ = Task

    def init_tasks_for_user(self, user):
        """Initializes all tasks for a new user. """
        with open(current_app.config['TASK_DATA_FILE'], 'r') as f:
            reader = csv.reader(f)
            num = 0
            task_ids = []
            for row in reader:
                if num > 0:
                    task = self.create(
                        category=row[0],
                        title=row[1],
                        task_date=row[2],
                        description=row[3],
                        tutorial=row[4],
                        resource=row[5],
                        image=row[7],
                        owner=user)
                    task_ids.append(task.id)
                num += 1

            # Set up related tasks.
            f.seek(0)
            k = 0
            for row in reader:
                if k > 0 and row[6]:
                    related_task_rows = row[6].split(',')
                    task = self.get(task_ids[k - 1])
                    for r in related_task_rows:
                        related_task = self.get(task_ids[int(r.strip()) - 2])
                        task.related_tasks.append(related_task)
                    self.save(task)
                k += 1

            #################################
            # This is used for testing scenarios.
            scenarios = ScenariosService()
            scenario1 = scenarios.get(1)
            scenario2 = scenarios.get(2)

            task1 = self.get(task_ids[0])
            task2 = self.get(task_ids[1])
            task3 = self.get(task_ids[2])

            task1.scenarios.append(scenario1)
            task1.scenarios.append(scenario2)
            self.save(task1)

            task2.scenarios.append(scenario1)
            task2.scenarios.append(scenario2)
            self.save(task2)

            task3.scenarios.append(scenario1)
            self.save(task3)
            #################################            

    def _preprocess_params(self, kwargs):
        """Override _preprocess_params to change enum string to int and
        parse datetime.
        """
        kwargs['status'] = self._maybe_cast_enum_string_to_int(
            TaskStatus, kwargs.get('status', 0))
        kwargs['category'] = self._maybe_cast_enum_string_to_int(
             TaskCategory, kwargs.get('category', 0))

        task_date = kwargs.get('task_date', None)
        if task_date and isinstance(task_date, basestring):
            kwargs['task_date'] = parser.parse(task_date)
        return kwargs

    def _maybe_cast_enum_string_to_int(self, enum_cls, v):
        try:
            return int(v)
        except ValueError:
            return enum_cls.get(v).value
            
