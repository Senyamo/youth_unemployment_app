from django.apps import AppConfig

class SkillsDevelopmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'skills_development'

    def ready(self):
        import skills_development.signals
