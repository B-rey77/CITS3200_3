from django.contrib.admin.apps import SimpleAdminConfig
from .admin_site import admin_site

def get_my_admin_site():
    return admin_site

class MyAdminConfig(SimpleAdminConfig):
    default_site = 'database.admin_apps.get_my_admin_site'

    def ready(self):
        super().ready()
        from .admin import AccountAdmin