from django.apps import AppConfig


class VuelosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vuelos'

    def ready(self):
        import vuelos.signals