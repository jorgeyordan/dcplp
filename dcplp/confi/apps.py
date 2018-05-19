from django.apps import AppConfig


class ConfiConfig(AppConfig):
    name = 'confi'

    def ready(self):
        import confi.signals # register the signals
