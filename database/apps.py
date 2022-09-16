from django.contrib.admin import apps
from django.apps import AppConfig

class DatabaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'database'
    label = 'database'
    verbose_name = 'Strep A Database'
