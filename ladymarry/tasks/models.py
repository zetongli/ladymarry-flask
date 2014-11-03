from ..core import db
from ..helpers import JsonSerializer
from ..libs.enum import Enum


# Enum definitions.
TaskStatus = Enum('TaskStatus',
                  NotDone=0,
                  Done=1,
                  OnHold=2)

TaskCategory = Enum('TaskCategory',
                    GetStarted=0,
                    Venue=1,
                    Guest=2,
                    PhotographyAndVideography=3,
                    AttireBeautyAndRing=4,
                    FoodToastAndEntertainment=5,
                    FlowerAndDecor=6,
                    FinishUp=7)

TaskCategory.addAlias('Get Started', 'GetStarted')
TaskCategory.addAlias('Photography & Videography', 'PhotographyAndVideography')
TaskCategory.addAlias('Attire, Beauty & Ring', 'AttireBeautyAndRing')
TaskCategory.addAlias('Flower & Decor', 'FlowerAndDecor')
TaskCategory.addAlias('Food, Toast & Entertainment',
                      'FoodToastAndEntertainment')
TaskCategory.addAlias('Finish Up', 'FinishUp')


# Relation tables.
related_tasks = db.Table(
    'related_tasks',
    db.Column('task_id', db.Integer(),
              db.ForeignKey('tasks.id', ondelete='cascade')),
    db.Column('related_task_id', db.Integer(),
              db.ForeignKey('tasks.id', ondelete='cascade')))

tasks_scenarios = db.Table(
    'tasks_scenarios',
    db.Column('task_id', db.Integer(),
              db.ForeignKey('tasks.id', ondelete='cascade')),
    db.Column('scenario_id', db.Integer(),
              db.ForeignKey('scenarios.id', ondelete='cascade')))

series_tasks = db.Table(
    'series_tasks',
    db.Column('task_id', db.Integer(),
              db.ForeignKey('tasks.id', ondelete='cascade')),
    db.Column('series_task_id', db.Integer(),
              db.ForeignKey('tasks.id', ondelete='cascade')))

tasks_vendors = db.Table(
    'tasks_vendors',
    db.Column('task_id', db.Integer(),
              db.ForeignKey('tasks.id', ondelete='cascade')),
    db.Column('vendor_id', db.Integer(),
              db.ForeignKey('vendors.id', ondelete='cascade')))


# Scenario.
class ScenarioJsonSerializer(JsonSerializer):
    __json_hidden__ = ['tasks']


class Scenario(ScenarioJsonSerializer, db.Model):
    __tablename__ = 'scenarios'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    when = db.Column(db.Text())
    description = db.Column(db.Text())
    image = db.Column(db.String(255))


# Task.
class TaskJsonSerializer(JsonSerializer):
    __json_hidden__ = ['related_tasks',
                       'prev_related_tasks',
                       'scenarios',
                       'owner']

    # For series tasks, we dump task id for each of them.
    __json_modifiers__ = {
        'series_tasks': lambda tasks, _: [dict(id=task.id) for task in tasks]
    }


class Task(TaskJsonSerializer, db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer(), primary_key=True)

    # Basic info.
    title = db.Column(db.String(255))
    task_date = db.Column(db.DateTime())
    status = db.Column(db.Integer(), default=0)
    category = db.Column(db.Integer(), default=0)
    owner_id = db.Column(db.Integer(),
                         db.ForeignKey('users.id', ondelete='cascade'))
    required = db.Column(db.Boolean(), default=True)
    # How many hours required.
    workload = db.Column(db.Integer(), default=0)
    # Position only makes sense within same category and month. Using float
    # to make it efficient to change order.
    position = db.Column(db.Float())
    scenarios = db.relationship(
        'Scenario',
        secondary=tasks_scenarios,
        backref=db.backref('tasks', lazy='dynamic'),
        lazy='dynamic')
    # This is used for task over multiple months. Series tasks don't include
    # itself.
    series_tasks = db.relationship(
        'Task',
        secondary=series_tasks,
        primaryjoin=(id == series_tasks.c.task_id),
        secondaryjoin=(id == series_tasks.c.series_task_id))

    # Task detailed info.
    note = db.Column(db.Text())
    description = db.Column(db.Text())
    tutorial = db.Column(db.Text())
    resource = db.Column(db.Text())
    image = db.Column(db.String(255))
    image_compress = db.Column(db.String(255))
    related_tasks = db.relationship(
        'Task',
        secondary=related_tasks,
        primaryjoin=(id == related_tasks.c.task_id),
        secondaryjoin=(id == related_tasks.c.related_task_id),
        backref=db.backref('prev_related_tasks', lazy='dynamic'),
        lazy='dynamic')

    vendors = db.relationship(
        'Vendor',
        secondary=tasks_vendors,
        backref=db.backref('tasks', lazy='dynamic'))
