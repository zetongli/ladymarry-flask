from flask import current_app
from flask.ext.script import Command, prompt, prompt_pass

from ..core import db
from ..models import *


class CreateDBCommand(Command):
    def run(self):
        db.create_all()


class DropDBCommand(Command):
    def run(self):
        db.drop_all()
        
