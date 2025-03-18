from django.apps import AppConfig

class CommonsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "commons"

    def ready(self):
        import commons.signals  # ✅ signals.py 불러오기
