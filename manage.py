from flask.ext.script import Manager

from ladymarry.api import create_app
from ladymarry.manage import *

manager = Manager(create_app())
manager.add_command('create_db', CreateDBCommand())
manager.add_command('drop_db', DropDBCommand())
manager.add_command('clear_db', ClearDBCommand())
manager.add_command('seed_db', SeedDBCommand())

manager.add_command('create_task', CreateTaskCommand())
manager.add_command('list_task', ListTaskCommand())
manager.add_command('delete_task', DeleteTaskCommand())
manager.add_command('refresh_data', RefreshDataCommand())


if __name__ == "__main__":
    manager.run()
