from django.apps import AppConfig

class ImageAppConfig(AppConfig):
    name = 'scigym.images'

    def ready(self):
        import scigym.images.signals
