from utils import read_tasks, assign_vendors
from ..models import Vendor
from ..tasks import TasksService


_REFRESHED_FIELDS = ['category', 'required', 'workload', 'description',
                     'tutorial', 'resource', 'image', 'image_compress']


class TaskRefresher(object):
    def __init__(self):
        self._tasks = TasksService()

    def refresh_tasks(self, user, task_file, vendor_file):
        if not user:
            return

        tasks = user.tasks.all()
        title_old_tasks = {task.title: task for task in tasks}

        new_tasks, _ = read_tasks(task_file)
        assign_vendors(new_tasks, vendor_file)
        title_new_tasks = {task.title: task for task in new_tasks}

        for title in title_old_tasks.keys():
            self._refresh_single_task(title_old_tasks[title],
                                      title_new_tasks.get(title, None))

    def _refresh_single_task(self, old_task, new_task):
        if not old_task or not new_task:
            return

        kvs = {k: getattr(new_task, k) for k in _REFRESHED_FIELDS}
        self._tasks.update(old_task, **kvs)

        # Update vendors.
        old_ids = set([v.id for v in old_task.vendors])
        new_ids = set([v.id for v in new_task.vendors])
        stale = False
        if len(old_ids) != len(new_ids):
            stale = True
        else:
            for old_id in old_ids:
                if old_id not in new_ids:
                    stale = True
                    break

        if stale:
            old_task.vendors[:] = new_task.vendors
            self._tasks.save(old_task)
        
