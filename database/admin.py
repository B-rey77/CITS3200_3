from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.template.loader import render_to_string
from django.urls import reverse

from admin_action_buttons.admin import ActionButtonsMixin

from database.models import Users, Studies, Results # Custom admin form imported from models.py

# The Custom Admin user model
class AccountAdmin(ActionButtonsMixin, UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'is_superuser')
    search_fields = ['email']
    readonly_fields = ('id', 'date_joined')
    
    ordering = ['email']
    
    filter_horizontal = ()
    list_filter = ('is_superuser', 'is_active',)
    fieldsets = ()

# override default behaviour to allow viewing by anyone
class ViewModelAdmin(ActionButtonsMixin, ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return request.user.is_active #and request.user.can_view_data
    
class StudiesAdmin(ViewModelAdmin):
    list_display = ('Paper_title', 'Year', 'Study_group', 'Unique_identifier', 'get_paper_link',
        'Disease', 'Study_description',
        'Case_definition','Case_findings', 'Data_source','Case_cap_meth',
        'Coverage','Jurisdiction', 'Climate', 'Aria_remote',
        'Population_group_strata',	'Age_original', 'Burden_measure', 'Notes')
    list_filter = ('Study_design', 'Study_group', 'Age_general', 'Jurisdiction', 'Climate', 'Aria_remote', 'Population_denom')
    ordering = ('Paper_title', )
    search_fields = ('Paper_title', 'Study_description')
    search_help_text = 'Search Titles or Descriptions matching keywords. Put quotes around search terms to find exact phrases only.'

    @admin.display(ordering='Paper_title', description='Link')
    def get_paper_link(self, obj):
        if not obj.Paper_link or obj.Paper_link.upper() == 'N/A':
            return 'N/A'
        return format_html('<a href="{}">Download</a>', obj.Paper_link)


class ResultsAdmin(ViewModelAdmin):
    @admin.display(ordering='Study__Paper_title', description='Study')
    def get_study(self, obj):
        if obj.Study:
            return format_html('<a href="{}">{}</a>',
                reverse('admin:database_studies_change', args=[obj.Study.id]),
                obj.Study.Paper_title,
            )

    @admin.display(ordering='Study__Study_group', description='Group')
    def get_study_group(self, obj):
        if obj.Study:
            return obj.Study.Study_group
        else:
            return 'Study Unknown'

    @admin.display(description='Disease Burden')
    def get_measure(self, obj):
        
        return format_html('<div><b>Burden: {}</b><br><br>Measure: {}</div>',
            obj.get_burden(), obj.Measure
        )

    @admin.display(description='Population')
    def get_population_html(self, obj):
        return format_html('<div><b>Gender: </b>{}</div><br><div><b>Indigenous: </b>{}<br>{}</div>',
            obj.Population_gender, obj.Indigenous_status, obj.Indigenous_population
        )
    
    @admin.display(description='Location')
    def get_location_html(self, obj):
        return format_html('<div><b>Country: </b>{}<br><b>Jurisdiction: </b>{}<br><b>Specific: </b>{}</div>',
            obj.Country, obj.Jurisdiction, obj.Specific_location
        )

    @admin.display(description='Flags')
    def get_flags_html(self, obj):
        return render_to_string('database/results_flags.html', context={'row': obj})

    @admin.display(description='Observation Time')
    def get_observation_time(self, obj):
        return format_html('<b>{} year{}</b><br>{} to {}',
            obj.Observation_time_years,
            '' if obj.Observation_time_years == 1 else 's',
            obj.Year_start,
            obj.Year_stop
        )
                

    # fvp: removed soem fields for demo: , 'Mortality_flag',	'Recurrent_ARF_flag','GAS_attributable_fraction', 'Defined_ARF', 'Focus_of_study', 
    list_display = ('get_measure', 'get_study_group', 'get_observation_time', 'get_age',
        'get_population_html', 'get_location_html', 'get_study', 'Notes', 'get_flags_html', )

    list_filter = ('Study__Study_group', 'Age_general', 'Age_original', 'Interpolated_from_graph', 'Age_standardisation', 'Dataset_name',
        'Proportion', 'Mortality_flag', 'Recurrent_ARF_flag', 'GAS_attributable_fraction', 'Defined_ARF')

    ordering = ('-Study__Study_group', )    

    search_fields = ('Study__Paper_title', 'Measure', 'Specific_location', 'Jurisdiction')
    search_help_text = 'Search Study Titles, Measure, Location or Jurisdiction for matching keywords. Put quotes around search terms to find exact phrases only.'



from database.admin_site import admin_site # Custom admin site

admin_site.register(Users, AccountAdmin)
admin_site.register(Studies, StudiesAdmin)
admin_site.register(Results, ResultsAdmin)
admin_site.unregister(Group)