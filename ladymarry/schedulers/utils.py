from collections import defaultdict

from ..models import Task
from ..tasks import TasksService
from ..utils import read_csv
from ..vendors import VendorsService


_tasks = TasksService()
_vendors = VendorsService()


def read_tasks(task_file, user=None):
    """Returns unsaved (tasks, task_index_to_task_indices). """
    tasks = []
    # Map <task index, related task indices>.
    task_index_to_task_indices = {}
    i = 0
    for row in read_csv(task_file):
        required = (row[9].lower() == 'required')
        task = _tasks.new(
            category=row[0],
            title=row[1],
            task_date=row[2],
            description=row[3],
            tutorial=row[4],
            resource=row[5],
            image=('/server/img/%s' % row[8]) if row[8] else row[7],
            image_compress=(
                '/server/img/%s' % _get_compressed_image_name(
                    row[8])) if row[8] else row[7],
            position=i if required else i + 1000, # Lower optional tasks.
            owner=user,
#           workload=int(row[10]),
            required=required)
        assert _is_task_valid(task)
                
        tasks.append(task)
        if row[6]:
            task_index_to_task_indices[i] = [int(k.strip()) - 2
                                             for k in row[6].split(',')]
        i += 1
    return tasks, task_index_to_task_indices

def assign_vendors(tasks, vendor_file):
    title_to_vendors = _read_vendors(vendor_file)

    for i in xrange(len(tasks)):
        for vendor in title_to_vendors.get(tasks[i].title, []):
            tasks[i].vendors.append(vendor)

def _read_vendors(vendor_file):
    """Returns (title, vendors). """
    vendors = _vendors.all()
    name_to_vendor = {v.name: v for v in vendors}

    title_to_vendors = defaultdict(list)
    for row in read_csv(vendor_file):
        for i in [1, 7, 13]:
            if not row[i]:
                break
            title_to_vendors[row[0]].append(
                _vendors.first(name=row[i]))
    return title_to_vendors

def _is_task_valid(task):
    if task.resource:
        resources = task.resource.split(',')
        for resource in resources:
            r = resource.split('|')
            if len(r) != 2:
                print 'Invalid resources: %s' % task.resource
                return False
    return True

def _get_compressed_image_name(name):
    """If name is 'abc.jpb', returns 'abc_compreseed.jpg'. """
    if '.' not in name:
        return None
    index = name.rfind('.')
    return name[: index] + '_compressed' + name[index:]

