from dateutil import parser

from flask import current_app

from ..core import Service
from ..utils import read_csv
from .models import Scenario, Task, TaskStatus, TaskCategory


class ScenariosService(Service):
    __model__ = Scenario

    def init_scenarios(self):
        """This should be called only once to create Scenario objects. """
        for row in read_csv(current_app.config['SCENARIO_DATA_FILE']):
            if not row[0]:
                continue
            scenario = self.create(
                title=row[0],
                when=row[1],
                description=row[2],
                image='/server/img/%s' % row[4])


class TasksService(Service):
    __model__ = Task

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
            date = parser.parse(task_date)
            # We need to make offset aware datetime offset naive.
            kwargs['task_date'] = date.replace(tzinfo=None)
        return kwargs

    def _maybe_cast_enum_string_to_int(self, enum_cls, v):
        try:
            return int(v)
        except ValueError:
            return enum_cls.get(v).value
            
