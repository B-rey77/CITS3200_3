from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from database.models import Users # Custom admin form imported from models.py

# Register your models here.


# The Custom Admin user model
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'is_admin', 'is_superuser')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined')
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
admin.site.register(Users, AccountAdmin)


