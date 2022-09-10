from django.contrib.admin import apps
from django.apps import AppConfig


class DatabaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'database'

class MyAdminConfig(apps.AdminConfig):
    default_site = 'database.admin_site.StrepAAdminSite'
    