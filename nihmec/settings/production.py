from .base import *
import environ
from django.core.management.utils import get_random_secret_key
import dj_database_url

ALLOWED_HOSTS = ["nihmec-production.up.railway.app", "nihmec.com"]
# DEBUG = False

try:
    from .local import *
except ImportError:
    pass

