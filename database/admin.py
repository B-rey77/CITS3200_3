from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from database.models import Users, Studies, Results # Custom admin form imported from models.py

# The Custom Admin user model
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'is_admin', 'is_superuser')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined')
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
# FVP: basic admin pages for studies, results (based on test models, will need to be updated when the proper set of fields is added)
class StudiesAdmin(ModelAdmin):
    list_display = ('Unique_identifier','Study_group','Paper_title','Paper_link','Year','Disease','Study_design','Study_design_other','Study_description','Case_definition','Case_findings','Case_findings_other','Data_source','Case_cap_meth','Case_cap_meth_other','Coverage','Jurisdiction','Specific_region',	'Climate',	'Aria_remote',	'Population_group_strata',	'Population_denom',	'Age_original',	'Age_general',	'Age_min',	'Age_max',	'Burden_measure',	'Ses_reported',	'Mortality_data',	'Method_limitations',	'Limitations_identified',	'Other_points')
    list_filter = ('Study_design', 'Study_group', 'Age_general')
    search_fields = ('Paper_title', 'Study_description')

class ResultsAdmin(ModelAdmin):
    list_display = ('Study', 'Age_general', 'Age_min', 'Age_max', 'Age_general', 'Age_min', 'Age_max', 'Age_original', 'Population_gender', 'Indigenous_status', 'Indigenous_population', 'Country', 'Jurisdiction', 'Specific_location', 'Year_start',	'Year_stop', 'Observation_time_years',	'Numerator', 'Denominator',	'Point_estimate', 'Measure', 'Interpolated_from_graph', 'Age_standardisation',	'Dataset_name',	'Proportion', 'Mortality_flag',	'Recurrent_ARF_flag','GAS_attributable_fraction', 'Defined_ARF', 'Focus_of_study',	'Notes')
    list_filter = ('Age_general', 'Interpolated_from_graph', 'Age_standardisation', 'Dataset_name', 'Proportion', 'Mortality_flag', 'Recurrent_ARF_flag', 'GAS_attributable_fraction', 'Defined_ARF')
    search_fields = ('Study', 'Age_general', 'Age_min', 'Age_max', 'Age_original', 'Year_start', 'Year_stop')


from database.admin_site import admin_site # Custom admin site

admin_site.register(Users, AccountAdmin)
admin_site.register(Studies, StudiesAdmin)
admin_site.register(Results, ResultsAdmin)
admin_site.unregister(Group)