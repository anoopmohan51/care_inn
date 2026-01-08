from django.apps import AppConfig


class WorkorderApiConfig(AppConfig):
    name = 'workorder_api'

    def ready(self):
        import workorder_api.signals.workorder_signals
