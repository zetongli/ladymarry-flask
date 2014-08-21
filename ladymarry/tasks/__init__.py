from dateutil import parser

from flask import abort

from ..core import Service
from .models import Task, TaskStatus, TaskCategory


class TasksService(Service):
    __model__ = Task

    def find_between_date(self, since=None, to=None):
        """Returns tasks whose date is between `since` and `to`. """
        query = Task.query
        try:
            if since:
                since = parser.parse(since)
                query = query.filter(Task.task_date >= since)
            if to:
                to = parser.parse(to)
                query = query.filter(Task.task_date <= to)
            return query.all()
        except TypeError:
            abort(404)

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
            
