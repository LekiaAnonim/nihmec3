from .base import *
import environ
from django.core.management.utils import get_random_secret_key
import dj_database_url

env = environ.Env()
environ.Env.read_env()

DEBUG = False

try:
    from .local import *
except ImportError:
    pass

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

