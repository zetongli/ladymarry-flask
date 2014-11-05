from flask import current_app

from task_initializer import TaskInitializer
from task_exporter import TaskExporter


class SchedulersService(object):
    """This is a combination service for scheduling tasks. """

    def schedule_tasks(self,
                       user,
                       task_file=None,
                       create_when_no_task=True):
        """Initializes and schedule all tasks for a new user. """
        if not task_file:
            task_file = current_app.config['TASK_DATA_FILE']

        task_initializer = TaskInitializer()
        task_initializer.schedule_tasks(
            user, task_file, create_when_no_task)

    def export_tasks(self, user, output=None):
        if not output:
            output = current_app.config['DEFAULT_EXPORT_FILE']

        task_exporter = TaskExporter()
        task_exporter.export_tasks(user, output)
        
