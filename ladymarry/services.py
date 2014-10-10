from .tasks import ScenariosService, TasksService
from .users import UsersService, WaitingUsersService


scenarios = ScenariosService()
tasks = TasksService()
users = UsersService()
waiting_users = WaitingUsersService()
