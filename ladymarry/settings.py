from datetime import timedelta


DEBUG = True
SECRET_KEY = 'super-secret-key'

SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost:3306/ladymarry'
CELERY_BROKER_URL = 'redis://localhost:6379/0'

JWT_AUTH_URL_RULE = '/auth'
JWT_EXPIRATION_DELTA = timedelta(days=7)
