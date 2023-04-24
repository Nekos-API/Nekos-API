from django.apps import AppConfig


class CharactersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "characters"

    def ready(self):
        import characters.signals