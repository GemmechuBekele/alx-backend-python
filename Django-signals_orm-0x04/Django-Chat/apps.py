from django.apps import AppConfig

class MessagingConfig(AppConfig):
    name = 'messaging'  # this should match your app folder name

    def ready(self):
        import messaging.signals

