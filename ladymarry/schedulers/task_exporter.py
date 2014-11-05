import csv

from ..libs.enum import Enum
from ..models import Task, TaskCategory
from ..tasks import TasksService
from ..utils import read_csv


class TaskExporter(object):
    """Exports user's schedule to csv. """

    def __init__(self):
        self._tasks = TasksService()

    def export_tasks(self, user, output):
        tasks = user.tasks.order_by(
            Task.category, Task.task_date, Task.position).all()
        with open(output, 'wb') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['Category',
                             'Title',
                             'Date',
                             'Description',
                             'Tutorial',
                             'Resource',
                             'Related tasks',
                             'Image',
                             'Image file name',
                             'Required',
                             'Workload'])

            for task in tasks:
                writer.writerow(self._task_to_row(task))

    def _task_to_row(self, task):
        return [TaskCategory.getByValue(task.category).name,
                task.title,
                '%d/%d/%d' % (task.task_date.month,
                              task.task_date.day,
                              task.task_date.year),
                task.description.encode('utf-8'),
                task.tutorial.encode('utf-8'),
                task.resource.encode('utf-8'),
                None,
                self._get_task_image_url(task),
                self._get_task_image_file(task),
                'Required' if task.required else 'Optional',
                task.workload]

    def _get_task_image_url(self, task):
        if '/server/img/' in task.image:
            return None
        return task.image

    def _get_task_image_file(self, task):
        if '/server/img/' in task.image:
            index = task.image.rfind('/')
            return task.image[index + 1: ]
        return None
        
