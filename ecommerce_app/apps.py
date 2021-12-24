from django.apps import AppConfig


class EcommerceAppConfig(AppConfig):
    name = 'ecommerce_app'

    def ready(self):
        # import signal handlers
        import ecommerce_app.signals
