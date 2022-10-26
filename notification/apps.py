from django.apps import AppConfig
from django.core.signals import request_finished


class NotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notification'

    def ready(self):
        from . import signals
