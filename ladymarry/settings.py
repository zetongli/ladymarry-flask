from datetime import timedelta


DEBUG = True
SECRET_KEY = 'super-secret-key'

SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost:3306/ladymarry'
CELERY_BROKER_URL = 'redis://localhost:6379/0'

# JWT configs.
JWT_AUTH_URL_RULE = '/auth'
JWT_EXPIRATION_DELTA = timedelta(days=90)

# Data configs.
TASK_DATA_FILE = './ladymarry/data/task_data.csv'
SCENARIO_DATA_FILE = './ladymarry/data/scenario_data.csv'
VENDOR_DATA_FILE = './ladymarry/data/vendor_data.csv'

DEFAULT_EXPORT_FILE = './ladymarry/data/export_task_data.csv'

