from django.apps import AppConfig
# myapp/apps.py
from wagtail.users.apps import WagtailUsersAppConfig


class RegistrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'registration'





class CustomUsersAppConfig(WagtailUsersAppConfig):
    user_viewset = "registration.viewsets.UserViewSet"
