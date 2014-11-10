import datetime
from collections import defaultdict

from utils import read_tasks, assign_vendors
from ..tasks import TasksService


# TODO: Generalize to any roman numbers.
ROMANS = [' I', ' II', ' III', ' IV', 'V']


class TaskInitializer(object):
    """Initializes and schedules tasks for new users. """

    def __init__(self):
        self._tasks = TasksService()

    def schedule_tasks(self,
                       user,
                       task_file,
                       vendor_file,
                       create_when_no_task):
        """Initializes all tasks for a new user.
        """
        if not user:
            return

        tasks = user.tasks.all()
        if not tasks and create_when_no_task:
            tasks, task_index_to_task_indices = read_tasks(
                task_file, user)
            assign_vendors(tasks, vendor_file)

            # Set up related tasks.
            # TODO: Enable this once content is correct.
            # for index, indices in task_index_to_task_indices.iteritems():
            #     task = tasks[index]
            #     for k in indices:
            #         task.related_tasks.append(tasks[k])

            # Set up series tasks.
            title_to_series_tasks = defaultdict(list)
            for i in xrange(len(tasks)):
                for r in ROMANS:
                    if tasks[i].title.endswith(r):
                        title = tasks[i].title.replace(r, '')
                        title_to_series_tasks[title].append(tasks[i])
            for _, series in title_to_series_tasks.iteritems():
                for i in xrange(len(series)):
                    task = series[i]
                    # Series tasks don't include itself.
                    series_tasks = series[:]
                    del series_tasks[i]
                    task.series_tasks = series_tasks

        tasks = self._adjust_time(user.wedding_date, tasks)
        for task in tasks:
            self._tasks.save(task)

    def _adjust_time(self, wedding_date, tasks):
        """NOTE: To reduce db requests, the input tasks are not necessarily
        stored in db, which means task.id may not exist.
        Returns the adjusted tasks (not saved).
        """
        if not tasks:
            return []

        # Generate adjusted months array based on the wedding date.
        adjusted_months = []
        now = datetime.date.today()
        date = self._increment_month_and_clear_day(now, 1)
        while date <= wedding_date.date():
            adjusted_months.append(date)
            date = self._increment_month_and_clear_day(date, 1)

        # Fine tune the begin and end month.
        if adjusted_months and wedding_date.day < 15:
            adjusted_months.pop()
        if now.day <= 15:
            adjusted_months.insert(0, datetime.date(now.year, now.month, 1))

        if not adjusted_months:
            return tasks

        # Group task by (month, category) and also get min and max date.
        month_category_to_tasks = defaultdict(list)
        set_fake_id = False
        min_date = None
        max_date = None
        for i in xrange(len(tasks)):
            task = tasks[i]
            min_date = task.task_date if not min_date else min(
                min_date, task.task_date)
            max_date = task.task_date if not max_date else max(
                max_date, task.task_date)

            # NOTE: If id is not set in task, we set a fake one, which is used
            # for lookup and will be deleted later.
            if task.id is None:
                task.id = i
                set_fake_id = True
            month_category_to_tasks[
                (task.task_date.month, task.category)].append(task)

        # For each task, calculate "precise month" for it, e.g. in 2nd month,
        # there are 2 tasks for category C, then task1 has precise month 2.33
        # and task2 has 2.66.
        # NOTE: 2nd month could be any month (10, 12), but the precise month is
        #       always 2.xx.
        id_to_precise_month = {}
        for month_category, task_buckets in month_category_to_tasks.iteritems():
            for i in xrange(len(task_buckets)):
                id_to_precise_month[task_buckets[i].id] = (
                    self._minus_month(task_buckets[i].task_date, min_date) +
                    1.0 * (i + 1) / (len(task_buckets) + 1))

        # Adjust date for each task.
        adjusted_month_span = (
            (1.0 * self._minus_month(max_date, min_date) + 1) /
            len(adjusted_months))
        for i in xrange(len(tasks)):
            precise_month = id_to_precise_month[tasks[i].id]
            adjusted_month_index = int(precise_month / adjusted_month_span)
            tasks[i].task_date = adjusted_months[adjusted_month_index]

            if set_fake_id:
                del tasks[i].id

        return tasks

    def _increment_month_and_clear_day(self, date, i):
        p, q = divmod(date.month + i - 1, 12)
        m = q + 1
        y = date.year + p
        return datetime.date(y, m, 1)

    def _minus_month(self, date1, date2):
        """Returns month diff of date1 - date2. """
        min_date = min(date1, date2)
        max_date = max(date1, date2)

        d_year = max_date.year - min_date.year
        d_month = max_date.month - min_date.month
        d = d_year * 12 + d_month
        return d if date1 == max_date else -d    
    
