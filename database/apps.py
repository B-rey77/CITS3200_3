from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class DatabaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'database'

class MyAdminConfig(AdminConfig):
    default_site = 'database.admin_site.StrepAAdminSite'