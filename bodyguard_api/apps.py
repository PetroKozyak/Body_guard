from django.apps import AppConfig


class BodyguardApiConfig(AppConfig):
    name = 'bodyguard_api'

    def ready(self):
        import bodyguard_api.signals