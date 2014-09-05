from dateutil import parser

from ..core import Service
from .models import Scenario, Task, TaskStatus, TaskCategory
from .scheduler import Scheduler


class ScenariosService(Service):
    __model__ = Scenario

    def init_scenarios(self):
        scheduler = Scheduler(self, TasksService())
        scheduler.init_scenarios()


class TasksService(Service):
    __model__ = Task

    def schedule_tasks_for_user(self, user):
        scheduler = Scheduler(ScenariosService(), self)
        scheduler.schedule_tasks(user)

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
            
