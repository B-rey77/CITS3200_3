from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html

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
    list_display = ('Paper_title', 'Year', 'Study_group', 'Unique_identifier', 'get_paper_link',
        'Disease', 'Study_description',
        'Case_definition','Case_findings', 'Data_source','Case_cap_meth',
        'Coverage','Jurisdiction', 'Climate', 'Aria_remote',
        'Population_group_strata',	'Age_original', 'Burden_measure')
    list_filter = ('Study_design', 'Study_group', 'Age_general', 'Jurisdiction', 'Climate', 'Aria_remote', 'Population_denom')
    ordering = ('Paper_title', )
    search_fields = ('Paper_title', 'Study_description')

    @admin.display(ordering='Paper_title', description='Link')
    def get_paper_link(self, obj):
        if not obj.Paper_link or obj.Paper_link.upper() == 'N/A':
            return 'N/A'
        return format_html('<a href="{}">Download</a>', obj.Paper_link)


class ResultsAdmin(ViewModelAdmin):
    @admin.display(ordering='Study__Paper_title', description='Study')
    def get_study(self, obj):
        return obj.Study.Paper_title

    @admin.display(ordering='Study__Study_group', description='Study Group')
    def get_study_group(self, obj):
        return obj.Study.Study_group

    @admin.display(description='Disease Burden')
    def get_measure(self, obj):
        
        return format_html('<div><b>Burden: {}</b><br><br>Measure: {}</div>',
            obj.get_burden(), obj.Measure
        )
    

                

    # fvp: removed soem fields for demo: , 'Mortality_flag',	'Recurrent_ARF_flag','GAS_attributable_fraction', 'Defined_ARF', 'Focus_of_study', 
    list_display = ('get_study_group', 'get_measure', 'get_age', 'Population_gender', 'Indigenous_population',
         'Country', 'Jurisdiction', 'Specific_location', 'Year_start',	'Year_stop', 'Observation_time_years',
         'Interpolated_from_graph', 'Age_standardisation',	'Dataset_name',	'Proportion', 'Notes', 'get_study')

    list_filter = ('Age_general', 'Age_original', 'Interpolated_from_graph', 'Age_standardisation', 'Dataset_name',
        'Proportion', 'Mortality_flag', 'Recurrent_ARF_flag', 'GAS_attributable_fraction', 'Defined_ARF')

    ordering = ('Study__Study_group', )    

    search_fields = ('Study__Paper_title', 'Measure', 'Specific_location', 'Jurisdiction',
        'Population_gender', 'Indigenous_population' )


from database.admin_site import admin_site # Custom admin site

admin_site.register(Users, AccountAdmin)
admin_site.register(Studies, StudiesAdmin)
admin_site.register(Results, ResultsAdmin)
admin_site.unregister(Group)