from django.apps import AppConfig


class BoutiqueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'boutique'
    
    def ready(self):
        """
        Importe les signals quand l'application est prête
        """
        import boutique.signals
