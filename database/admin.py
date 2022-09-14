from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from database.models import Users, Studies, Results # Custom admin form imported from models.py

# The Custom Admin user model
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'is_active', 'is_superuser')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined')
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# override default behaviour to allow viewing by anyone
class ViewModelAdmin(ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return request.user.is_active and request.user.can_view_data
    
    
# FVP: basic admin pages for studies, results (based on test models, will need to be updated when the proper set of fields is added)
class StudiesAdmin(ViewModelAdmin):
    list_display = ('Paper_title', 'Year', 'Study_design', 'Study_group', 'Age_general', 'Unique_identifier')
    list_filter = ('Year', 'Study_design', 'Study_group', 'Age_general')
    search_fields = ('Paper_title', 'Study_description')

class ResultsAdmin(ViewModelAdmin):
    list_display = ('Study', 'Year_start', 'Year_stop', 'Age_general',
        'Population_gender', 'Indigenous_status', 'Jurisdiction', 'Country',
        'Point_estimate', 'Numerator', 'Denominator')
    list_filter = ('Study', 'Study__Study_group', 'Age_general', 'Age_original', 'Year_start', 'Year_stop')
    search_fields = ('Study__Paper_title', 'Country', 'Jurisdiction', 'Specific_location', 'Measure', 'Defined_ARF', 'Focus_of_study', 'Notes')


from database.admin_site import admin_site # Custom admin site

admin_site.register(Users, AccountAdmin)
admin_site.register(Studies, StudiesAdmin)
admin_site.register(Results, ResultsAdmin)
admin_site.unregister(Group)