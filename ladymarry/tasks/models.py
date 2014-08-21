from ..core import db
from ..helpers import JsonSerializer
from ..libs.enum import Enum


TaskStatus = Enum('TaskStatus',
                  Undo=0,
                  Done=1,
                  OnHold=2)

TaskCategory = Enum('TaskCategory',
                    Overall=0,
                    PartiesAndEntertainment=1,
                    Venue=2,
                    FashionAndBeauty=3,
                    GuestAndGuestlist=4,
                    PhotographyAndVideography=5,
                    FlowerAndDecor=6,
                    Music=7,
                    CateringAndCake=8,
                    SpeechAndToast=9,
                    Honeymoon=10)
TaskCategory.addAlias('Parties & Entertainment', 'PartiesAndEntertainment')
TaskCategory.addAlias('Fashion & Beauty', 'FashionAndBeauty')
TaskCategory.addAlias('Guest & Guestlist', 'GuestAndGuestlist')
TaskCategory.addAlias('Photography & Videography', 'PhotographyAndVideography')
TaskCategory.addAlias('Flower & Decor', 'FlowerAndDecor')
TaskCategory.addAlias('Catering & Cake', 'CateringAndCake')
TaskCategory.addAlias('Speech & Toast', 'SpeechAndToast')


# related_tasks = db.Table(
#     'related_tasks',
#     db.Column('task_id', db.Integer(), db.ForeignKey('tasks.id')),
#     db.Column('related_task_id', db.Integer(), db.ForeignKey('tasks.id')))


class TaskJsonSerializer(JsonSerializer):
    pass


class Task(TaskJsonSerializer, db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer(), primary_key=True)

    # Basic info.
    title = db.Column(db.String(255))
    task_date = db.Column(db.DateTime())
    status = db.Column(db.Integer(), default=0)
    category = db.Column(db.Integer(), default=0)
    priority = db.Column(db.Integer(), default=0)

    # Task detailed info.
    description = db.Column(db.Text())
    tutorial = db.Column(db.Text())
    resource = db.Column(db.Text())
    image = db.Column(db.String(255))
    # related_tasks = db.relationship(
    #     'Task',
    #     secondary=related_tasks,
    #     primaryjoin=id==related_tasks.c.task_id,
    #     secondaryjoin=id==related_tasks.c.related_task_id,
    #     backref=db.backref('prev_related_tasks', lazy='dynamic'),
    #     lazy='dynamic')
    
