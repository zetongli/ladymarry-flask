from flask import json
from flask.ext.script import Command, prompt

from ..services import vendors


class ImportVendorCommand(Command):
    def run(self):
        clear_exist = prompt('Clear existing vendors? (y or n)')
        vendors.init_vendors((clear_exist == 'y'))
            


