from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from database.models import Users, Study, Results # Custom admin form imported from models.py

# The Custom Admin user model
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'is_admin', 'is_superuser')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined')
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
# FVP: basic admin pages for studies, results (based on test models, will need to be updated when the proper set of fields is added)
class StudyAdmin(ModelAdmin):
    list_display = ('title', 'pub_year', 'identifier')
    list_filter = ('pub_year', )
    search_fields = ('title', )

class ResultsAdmin(ModelAdmin):
    list_display = ('study', 'point_estimate', 'numerator', 'denominator', 'measure')
    list_filter = ('study', 'ages', 'year_start', 'year_stop')
    search_fields = ('study__title', 'measure')


from database.admin_site import admin_site # Custom admin site

admin_site.register(Users, AccountAdmin)
admin_site.register(Study, StudyAdmin)
admin_site.register(Results, ResultsAdmin)
admin_site.unregister(Group)