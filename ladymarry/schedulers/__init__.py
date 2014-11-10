from flask import current_app

from task_refresher import TaskRefresher
from task_initializer import TaskInitializer
from task_exporter import TaskExporter


class SchedulersService(object):
    """This is a combination service for scheduling tasks. """

    def schedule_tasks(self,
                       user,
                       task_file=None,
                       vendor_file=None,
                       create_when_no_task=True):
        """Initializes and schedule all tasks for a new user. """
        if not task_file:
            task_file = current_app.config['TASK_DATA_FILE']
        if not vendor_file:
            vendor_file = current_app.config['VENDOR_DATA_FILE']

        task_initializer = TaskInitializer()
        task_initializer.schedule_tasks(
            user, task_file, vendor_file, create_when_no_task)

    def export_tasks(self, user, output=None):
        if not output:
            output = current_app.config['DEFAULT_EXPORT_FILE']

        task_exporter = TaskExporter()
        task_exporter.export_tasks(user, output)

    def refresh_tasks(self, user, task_file=None, vendor_file=None):
        if not task_file:
            task_file = current_app.config['TASK_DATA_FILE']
        if not vendor_file:
            vendor_file = current_app.config['VENDOR_DATA_FILE']

        task_refresher = TaskRefresher()
        task_refresher.refresh_tasks(user, task_file, vendor_file)
