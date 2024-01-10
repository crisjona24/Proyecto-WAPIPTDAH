from django.apps import AppConfig


class AppwapiptdaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'APPWapiptda'

    # Registro de signals
    def ready(self):
        super().ready()
        self.registrar_senales()

    def registrar_senales(self):
        import APPWapiptda.signals  # Importa el archivo signals.py
