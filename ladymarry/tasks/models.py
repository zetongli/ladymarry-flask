from ..core import db
from ..helpers import JsonSerializer
from ..libs.enum import Enum


# Enum definitions.
TaskStatus = Enum('TaskStatus',
                  NotDone=0,
                  Done=1,
                  OnHold=2)

TaskCategory = Enum('TaskCategory',
                    Overall=0,
                    PartiesAndEntertainment=1,
                    Venue=2,
                    AttireAndBeauty=3,
                    GuestAndGuestlist=4,
                    PhotographyAndVideography=5,
                    FlowerAndDecor=6,
                    Music=7,
                    CateringAndCake=8,
                    SpeechAndToast=9,
                    Tradition=10,
                    Honeymoon=11)
TaskCategory.addAlias('Parties & Entertainment', 'PartiesAndEntertainment')
TaskCategory.addAlias('Attire & Beauty', 'AttireAndBeauty')
TaskCategory.addAlias('Guest & Guestlist', 'GuestAndGuestlist')
TaskCategory.addAlias('Photography & Videography', 'PhotographyAndVideography')
TaskCategory.addAlias('Flower & Decor', 'FlowerAndDecor')
TaskCategory.addAlias('Catering & Cake', 'CateringAndCake')
TaskCategory.addAlias('Speech & Toast', 'SpeechAndToast')


# Relation tables.
related_tasks = db.Table(
    'related_tasks',
    db.Column('task_id', db.Integer(), db.ForeignKey('tasks.id')),
    db.Column('related_task_id', db.Integer(), db.ForeignKey('tasks.id')))

tasks_scenarios = db.Table(
    'tasks_scenarios',
    db.Column('task_id', db.Integer(), db.ForeignKey('tasks.id')),
    db.Column('scenario_id', db.Integer(), db.ForeignKey('scenarios.id')))


# Scenario.
class ScenarioJsonSerializer(JsonSerializer):
    __json_hidden__ = ['tasks']


class Scenario(ScenarioJsonSerializer, db.Model):
    __tablename__ = 'scenarios'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    when = db.Column(db.Text())
    description = db.Column(db.Text())


# Task.
class TaskJsonSerializer(JsonSerializer):
    __json_hidden__ = ['related_tasks',
                       'prev_related_tasks',
                       'scenarios',
                       'owner']


class Task(TaskJsonSerializer, db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer(), primary_key=True)

    # Basic info.
    title = db.Column(db.String(255))
    task_date = db.Column(db.DateTime())
    status = db.Column(db.Integer(), default=0)
    category = db.Column(db.Integer(), default=0)

    scenarios = db.relationship(
        'Scenario',
        secondary=tasks_scenarios,
        backref=db.backref('tasks', lazy='dynamic'),
        lazy='dynamic')

    owner_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    # Task detailed info.
    description = db.Column(db.Text())
    tutorial = db.Column(db.Text())
    resource = db.Column(db.Text())
    image = db.Column(db.String(255))
    related_tasks = db.relationship(
        'Task',
        secondary=related_tasks,
        primaryjoin=(id == related_tasks.c.task_id),
        secondaryjoin=(id == related_tasks.c.related_task_id),
        backref=db.backref('prev_related_tasks', lazy='dynamic'),
        lazy='dynamic')
