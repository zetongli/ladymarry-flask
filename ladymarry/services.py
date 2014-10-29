from .schedulers import SchedulersService
from .tasks import ScenariosService, TasksService
from .users import UsersService, WaitingUsersService
from .vendors import VendorsService


scenarios = ScenariosService()
tasks = TasksService()
users = UsersService()
waiting_users = WaitingUsersService()
vendors = VendorsService()
schedulers = SchedulersService()
