from .base import *
import environ
from django.core.management.utils import get_random_secret_key
import dj_database_url

env = environ.Env(
    DEBUG=(bool, False)
)

ALLOWED_HOSTS = ["nihmec3-production-4951.up.railway.app", "nihmec.com"]
DEBUG = env('DEBUG')


EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env('DEFAULT_FROM_EMAIL')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

DATABASES = {
    "default": dj_database_url.config(default='postgresql://postgres:afAe6Ffdfb1bc3c3b233D6fGGabgefdC@roundhouse.proxy.rlwy.net:13514/railway', conn_max_age=1800),
}

PAYSTACK_SECRET_KEY = env('PAYSTACK_SECRET_KEY')
PAYSTACK_PUBLIC_KEY = ""

import cloudinary
          
# cloudinary.config( 
#   cloud_name = env("cloud_name"), 
#   api_key = env("cloudinary_api_key"), 
#   api_secret = env("cloudinary_api_secret") 
# )

try:
    from .local import *
except ImportError:
    pass

