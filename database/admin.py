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
    
class StudiesAdmin(ViewModelAdmin):
    list_display = ('Unique_identifier','Study_group','Paper_title','Paper_link',
        'Year','Disease','Study_design','Study_design_other','Study_description',
        'Case_definition','Case_findings','Case_findings_other','Data_source','Case_cap_meth',
        'Case_cap_meth_other','Coverage','Jurisdiction','Specific_region',	'Climate',	'Aria_remote',
        'Population_group_strata',	'Population_denom',	'Age_original', 'Burden_measure',	'Ses_reported',	'Mortality_data',
        'Method_limitations',	'Limitations_identified',	'Other_points')
    list_filter = ('Study_design', 'Study_group', 'Age_general', 'Jurisdiction', 'Climate', 'Aria_remote', 'Population_denom')
    search_fields = ('Paper_title', 'Study_description')

class ResultsAdmin(ViewModelAdmin):
    def get_study(self, obj):
        return obj.Study.Paper_title

    def get_study_group(self, obj):
        return obj.Study.Study_group
    # fvp: removed soem fields for demo: , 'Mortality_flag',	'Recurrent_ARF_flag','GAS_attributable_fraction', 'Defined_ARF', 'Focus_of_study', 
    list_display = ('get_study', 'get_study_group', 'Age_general', 'Population_gender', 'Indigenous_population',
         'Country', 'Jurisdiction', 'Specific_location', 'Year_start',	'Year_stop', 'Observation_time_years',	'Numerator', 'Denominator',
    	'Point_estimate', 'Measure', 'Interpolated_from_graph', 'Age_standardisation',	'Dataset_name',	'Proportion', 'Notes')
    list_filter = ('Age_general', 'Age_original', 'Interpolated_from_graph', 'Age_standardisation', 'Dataset_name',
        'Proportion', 'Mortality_flag', 'Recurrent_ARF_flag', 'GAS_attributable_fraction', 'Defined_ARF')
    search_fields = ('Study__Paper_title', 'Measure', 'Specific_location', 'Jurisdiction',
        'Population_gender', 'Indigenous_population' )

from database.admin_site import admin_site # Custom admin site

admin_site.register(Users, AccountAdmin)
admin_site.register(Studies, StudiesAdmin)
admin_site.register(Results, ResultsAdmin)
admin_site.unregister(Group)