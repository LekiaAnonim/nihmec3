from .base import *
from django.core.management.utils import get_random_secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# EMAIL_HOST_USER = os.getenv('DEFAULT_FROM_EMAIL')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')

try:
    from .local import *
except ImportError:
    pass
