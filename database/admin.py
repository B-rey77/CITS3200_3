from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.template.loader import render_to_string
from django.urls import reverse
from rangefilter.filters import NumericRangeFilter
from admin_action_buttons.admin import ActionButtonsMixin

from database.models import Users, Studies, Results, proxies, is_approved_proxies # Custom admin form imported from models.py
from .actions import download_as_csv
from django_admin_listfilter_dropdown.filters import (DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter)
from django.db import models
        
# The Custom Admin user model
class AccountAdmin(ActionButtonsMixin, UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'is_superuser')
    search_fields = ['email']
    readonly_fields = ('id', 'date_joined')
    actions = [download_as_csv('Export selected accounts to CSV')]
    
    ordering = ['email']
    
    filter_horizontal = ()
    list_filter = ('is_superuser', 'is_active',)
    fieldsets = ()

# override default behaviour to allow viewing by anyone
class ViewModelAdmin(ActionButtonsMixin, ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return request.user.is_active #and request.user.can_view_data

    def has_add_permission(self, request, obj=None):
        return request.user.is_active #and request.user.can_add_data
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_approved=True)
           
    # save email of user that's adding studies/results
    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)
    
    # exclude fields so they're not viewable by generic users
    def get_exclude(self, request, obj=None):
            is_superuser = request.user.is_superuser
            excluded = ['added_by']
            if not is_superuser:
                return excluded

def get_age_html(obj):
    if obj.Age_min is not None and obj.Age_min > 0:
        if obj.Age_max is not None and obj.Age_max < 999:
            res = '%d to %d years old' % (obj.Age_min, obj.Age_max)
        else:
            res = '%d years and older' % obj.Age_min
    elif obj.Age_max is not None and obj.Age_max < 999:
        res = 'Up to %d years old' % obj.Age_max
    else:
        res = None
    
    if res:
        return format_html('<b>{}</b> ({})<br>{}', obj.Age_original, obj.Age_general, res)
    else:
        return format_html('<b>{}</b> ({})', obj.Age_original, obj.Age_general)

class ResultsInline(admin.StackedInline):
    model = Results
    extra = 0
    readonly_fields = ('is_approved',)
    
    def get_readonly_fields(self, request, obj=None):
            is_superuser = request.user.is_superuser
            if is_superuser:
                return []
            return self.readonly_fields
    
    def has_view_permission(self, request, obj=None):
        return True #and request.user.can_add_data
    
    def has_add_permission(self, request, obj=None):
        return True #and request.user.can_add_data
    
    # exclude fields so they're not viewable by generic users    
    def get_exclude(self, request, obj=None):
            is_superuser = request.user.is_superuser
            excluded = ['is_approved', 'added_by']
            if not is_superuser:
                return excluded
   
class StudiesAdmin(ViewModelAdmin):
    inlines = [ResultsInline]
    readonly_fields = ('is_approved',)
    
    def get_readonly_fields(self, request, obj=None):
            is_superuser = request.user.is_superuser
            if is_superuser:
                return []
            return self.readonly_fields
            
    list_display = ('Paper_title', 'get_info_html', 'get_location_html', 'get_population_html', 'get_age_html',
        'get_case_html', 'Burden_measure', 'Notes', 'get_flags_html')
    list_filter = (
        ('Study_design', ChoiceDropdownFilter), 
        ('Study_group',ChoiceDropdownFilter), 
        ('Age_general', DropdownFilter), 
        ('Age_min', NumericRangeFilter),
        ('Age_max', NumericRangeFilter),
        ('Coverage', DropdownFilter),
        ('Jurisdiction', DropdownFilter),
        ('Surveillance_setting', DropdownFilter),
        ('Climate', DropdownFilter), 
        ('Aria_remote', DropdownFilter),
        ('Population_denom', DropdownFilter),
        ('Population_group_strata', DropdownFilter),
         'Ses_reported', 'Mortality_data', 'Method_limitations')
    ordering = ('Paper_title', 'Study_group')
    search_fields = ('Paper_title', 'Study_description', 'Age_general', 'Jurisdiction')
    actions = [download_as_csv('Export selected Studies to CSV')]
    search_help_text = 'Search Titles or Descriptions matching keywords. Put quotes around search terms to find exact phrases only.'

    @admin.display(ordering='Year', description='Study Info')
    def get_info_html(self, obj):
        return render_to_string('database/studies_info.html', context={'row': obj})

    @admin.display(description='Flags')
    def get_flags_html(self, obj):
        return render_to_string('database/row_flags.html', context={'row': obj})
    
    @admin.display(description='Population')
    def get_population_html(self, obj):
        return format_html('<div><b>Group Strata: </b>{}</div><br><div><b>Denom: </b>{}</div>',
            obj.Population_group_strata, obj.Population_denom
        )
    
    @admin.display(description='Geography', ordering='Specific_region')
    def get_location_html(self, obj):
        return format_html('<div><b>Specific Region: </b>{}<br><b>Jurisdiction: </b>{}<br>'
            '<b>Aria Remote: </b>{}<br><b>Climate: </b>{}<br><b>Coverage: </b>{}</div>',
            obj.Specific_region, obj.Jurisdiction,
            obj.Aria_remote, obj.Climate, obj.Coverage
        )

    @admin.display(description='Case Info', ordering='Case_definition')
    def get_case_html(self, obj):
        return format_html('<div><b>Case Definition: </b>{}<br><b>Surveillance: </b>{}<br>'
            '<b>Case Findings: </b>{}<br><b>Data Source: </b>{}</div>',
            obj.Case_definition, obj.Surveillance_setting, obj.Case_findings, obj.Data_source,
        )

    @admin.display(ordering='Age_general', description='Age Bracket')
    def get_age_html(self, obj):
        return get_age_html(obj)

    # save email of user that's adding studies inline
    def save_formset(self, request, obj, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.added_by = request.user
            instance.save()
            formset.save()


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
        return format_html('<div><b>Numerator: </b>{}<br><b>Denominator: </b>{}<br><b>Point estimate: </b>{}<br><br>Measure: {}</div>',
            obj.Numerator, obj.Denominator, obj.Point_estimate, obj.Measure
        )

    @admin.display(description='Population', ordering='Population_gender')
    def get_population_html(self, obj):
        return format_html('<div><b>Gender: </b>{}</div><br><div><b>Indigenous: </b>{}</div>',
            obj.Population_gender, obj.Indigenous_population
        )
    
    @admin.display(description='Location', ordering='Specific_location')
    def get_location_html(self, obj):
        return format_html('<div><b>Specific: </b>{}<br><b>Jurisdiction: </b>{}<br><b>Country: </b>{}</div>',
            obj.Specific_location, obj.Jurisdiction, obj.Country,
        )

    @admin.display(description='Flags')
    def get_flags_html(self, obj):
        return render_to_string('database/row_flags.html', context={'row': obj})

    @admin.display(description='Observation Time')
    def get_observation_time(self, obj):
        return format_html('<b>{} year{}</b><br>{} to {}',
            obj.Observation_time_years,
            '' if obj.Observation_time_years == 1 else 's',
            obj.Year_start,
            obj.Year_stop
        )

    @admin.display(ordering='Age_general', description='Age Bracket')
    def get_age_html(self, obj):
        return get_age_html(obj)

    # fvp: removed soem fields for demo: , 'Mortality_flag',	'Recurrent_ARF_flag','GAS_attributable_fraction', 'Defined_ARF', 'Focus_of_study', 
    readonly_fields = ('is_approved',)
    
    def get_readonly_fields(self, request, obj=None):
            is_superuser = request.user.is_superuser
            if is_superuser:
                return []
            return self.readonly_fields
    
    list_display = ('get_measure', 'get_study_group', 'get_observation_time', 'get_age_html',
        'get_population_html', 'get_location_html', 'get_study', 'Notes', 'get_flags_html', )

    list_filter = (
        ('Study__Study_group',ChoiceDropdownFilter), 
        ('Age_general', DropdownFilter),
        ('Age_min', NumericRangeFilter),
        ('Age_max', NumericRangeFilter),
        ('Numerator', NumericRangeFilter),
        ('Denominator', NumericRangeFilter),
        ('Point_estimate', NumericRangeFilter),
        ('Population_gender', DropdownFilter), 
        ('Jurisdiction', DropdownFilter),
        ('Indigenous_population', DropdownFilter),
        'Indigenous_status',
        'Interpolated_from_graph', 
        'Age_standardisation',
         'Dataset_name',
        'Proportion', 'Mortality_flag', 'Recurrent_ARF_flag', 'GAS_attributable_fraction', 'Defined_ARF')

    ordering = ('-Study__Study_group', )    
    actions = [download_as_csv('Export selected results to CSV')]

    search_fields = ('Study__Paper_title', 'Measure', 'Specific_location', 'Jurisdiction', 'Age_general')
    search_help_text = 'Search Study Titles, Measure, Location or Jurisdiction for matching keywords. Put quotes around search terms to find exact phrases only.'
    
from database.admin_site import admin_site # Custom admin site

admin_site.register(Users, AccountAdmin)
admin_site.register(Studies, StudiesAdmin)
admin_site.register(Results, ResultsAdmin)
admin_site.unregister(Group)



def get_proxy_admin(model, base_admin):
    """ create generic admin pages for different results/study groups """
    class AnythingProxyAdmin(base_admin):
        list_display = [
            x for x in base_admin.list_display if x not in {'get_study_group', 'Study_group'}
        ]
        list_filter = [
            x for x in base_admin.list_filter if x not in {'Study__Study_group', 'Study_group'}
        ]
        
        def has_add_permission(self, request):
            # don't confuse users by letting them add "specific group" results/studies,
            # since the proxy admin doesn't actually constrain which group the result belongs to.
            return False

    return AnythingProxyAdmin

def register_proxy_admins():
    for p in proxies:
        model_admin = get_proxy_admin(p, ResultsAdmin if issubclass(p, Results) else StudiesAdmin)
        admin_site.register(p, model_admin)

register_proxy_admins()

# Proxy models for data not approved - viewable by superusers only
def get_proxy_is_approved_admin(model, base_admin):
    """ create generic admin pages for different results/study groups """
    class UnapprovedProxyAdmin(base_admin):
        list_display = [
            x for x in base_admin.list_display if x not in {'get_study_group', 'Study_group'}
        ]
        list_filter = [
            x for x in base_admin.list_filter if x not in {'Study__Study_group', 'Study_group'}
        ]
        
        # don't confuse users by letting them add "specific group" results/studies,
        # since the proxy admin doesn't actually constrain which group the result belongs to.
        def has_module_permission(self, request):
            if not request.user.is_superuser:
                return False
            return True
        
        def has_add_permission(self, request):
            return False
            
    return UnapprovedProxyAdmin

def register_proxy_is_approved_admins():
    for p in is_approved_proxies:
        model_admin = get_proxy_is_approved_admin(p, ResultsAdmin if issubclass(p, Results) else StudiesAdmin)
        
        admin_site.register(p, model_admin)

register_proxy_is_approved_admins()
