import csv
import datetime
from collections import defaultdict

from flask import current_app

from .models import Scenario, Task


class Scheduler(object):

    def __init__(self, scenarios, tasks):
        self._scenarios = scenarios
        self._tasks = tasks

    def schedule_tasks(self, user):
        """Initializes all tasks for a new user. """
        if not user:
            return

        # Create tasks.
        tasks = []
        # Map <task index, related task indices>.
        index_to_task_indices = {}
        i = 0
        for row in self._read_csv(current_app.config['TASK_DATA_FILE']):
            task = self._tasks.new(
                category=row[0],
                title=row[1],
                task_date=row[2],
                description=row[3],
                tutorial=row[4],
                resource=row[5],
                image=row[7],
                owner=user)
            tasks.append(task)
            if row[6]:
                index_to_task_indices[i] = [int(k.strip()) - 2
                                            for k in row[6].split(',')]
            i += 1

        # Set up related tasks.
        for index, indices in index_to_task_indices.iteritems():
            task = tasks[index]
            for k in indices:
                task.related_tasks.append(tasks[k])

        tasks = self.adjust_time(user.wedding_date, tasks)
        tasks = [self._tasks.save(task) for task in tasks]

        #################################
        # This is used for testing scenarios.
        scenario1 = self._scenarios.get(1)
        scenario2 = self._scenarios.get(2)

        task1 = self._tasks.get(tasks[0].id)
        task2 = self._tasks.get(tasks[1].id)
        task3 = self._tasks.get(tasks[2].id)

        task1.scenarios.append(scenario1)
        task1.scenarios.append(scenario2)
        self._tasks.save(task1)

        task2.scenarios.append(scenario1)
        task2.scenarios.append(scenario2)
        self._tasks.save(task2)

        task3.scenarios.append(scenario1)
        self._tasks.save(task3)
        #################################

    def adjust_time(self, wedding_date, tasks):
        """NOTE: To reduce db requests, the input tasks are not necessarily
        stored in db, which means task.id may not exist.
        """
        now = datetime.datetime.now()
        elapsedTime = wedding_date - now

        # Generate adjusted months array based on the wedding date.
        num_months = int(elapsedTime.total_seconds() / (30 * 24 * 60 * 60))
        adjusted_months = []
        for i in xrange(num_months):
            adjusted_months.append(
                self._increment_month_and_clear_day(now, i + 1))
        if now.day < 15:
            num_months += 1
            adjusted_months.insert(0, datetime.date(now.year, now.month, 1))

        if num_months <= 0:
            return tasks

        # For each task, calculate "precise month" for it, e.g. in month 2,
        # there are 2 tasks for category C, then task1 has precise month 2.33
        # and task2 has 2.66.
        month_category_to_tasks = defaultdict(list)
        set_fake_id = False
        for i in xrange(len(tasks)):
            task = tasks[i]

            # NOTE: If id is not set in task, we set a fake one, which is used
            # for lookup and will be deleted later.
            if task.id is None:
                task.id = i
                set_fake_id = True
            month_category_to_tasks[
                (task.task_date.month, task.category)].append(task)

        id_to_precise_month = {}
        for month_category, task_buckets in month_category_to_tasks.iteritems():
            for i in xrange(len(task_buckets)):
                id_to_precise_month[task_buckets[i].id] = (
                    float(month_category[0]) +
                    1.0 * (i + 1) / (len(task_buckets) + 1))

        # Adjust date for each task.
        adjusted_month_span = 12.0 / num_months
        for i in xrange(len(tasks)):
            precise_month = id_to_precise_month[tasks[i].id]
            adjusted_month_index = int(
                (precise_month - 1) / adjusted_month_span)
            tasks[i].task_date = adjusted_months[adjusted_month_index]

            if set_fake_id:
                del tasks[i].id
        return tasks

    def _increment_month_and_clear_day(self, date, i):
        p, q = divmod(date.month + i - 1, 12)
        m = q + 1
        y = date.year + p
        return datetime.date(y, m, 1)

    def _read_csv(self, filename):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            num = 0
            for row in reader:
                if num > 0:
                    yield row
                num += 1
    
    
