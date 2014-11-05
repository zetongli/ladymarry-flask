from .schedulers import SchedulersService
from .tasks import TasksService
from .users import UsersService, WaitingUsersService
from .vendors import VendorsService


tasks = TasksService()
users = UsersService()
waiting_users = WaitingUsersService()
vendors = VendorsService()
schedulers = SchedulersService()
