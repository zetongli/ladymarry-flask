from dateutil import parser

from flask import current_app

from ..core import Service
from ..utils import read_csv
from .models import Task, TaskStatus, TaskCategory


class TasksService(Service):
    __model__ = Task

    def _preprocess_params(self, kwargs):
        """Override _preprocess_params to change enum string to int and
        parse datetime.
        """
        if 'status' in kwargs:
            kwargs['status'] = self._maybe_cast_enum_string_to_int(
                TaskStatus, kwargs['status'])
        if 'category' in kwargs:
            kwargs['category'] = self._maybe_cast_enum_string_to_int(
                TaskCategory, kwargs['category'])

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
            
