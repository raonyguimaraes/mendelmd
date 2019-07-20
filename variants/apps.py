from django.apps import AppConfig


class VariantsConfig(AppConfig):
    name = 'variants'

    def ready(self):
        import variants.signals
