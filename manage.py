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

manager.add_command('list_waiting_user', ListWaitingUserCommand())
manager.add_command('delete_waiting_user', DeleteWaitingUserCommand())

manager.add_command('list_user', ListUserCommand())
manager.add_command('delete_user', DeleteUserCommand())
manager.add_command('get_task_for_user', GetTaskForUserCommand())
manager.add_command('update_task_for_user', UpdateTaskForUserCommand())
manager.add_command('delete_task_for_user', DeleteTaskForUserCommand())

manager.add_command('import_vendor', ImportVendorCommand())


if __name__ == "__main__":
    manager.run()
