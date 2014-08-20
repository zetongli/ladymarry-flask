from ..core import Service
from .models import Task


class TasksService(Service):
    __model__ = Task
