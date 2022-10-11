from email.policy import default
from tabnanny import verbose
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib import admin
from django.conf import settings

# Create your models here.

class CustomAccountManager(BaseUserManager):
    
    def create_superuser(self, email, first_name, last_name, password, **other_fields):
    
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True')
        
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, 
                          **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_user(self, email, first_name, last_name, password, **other_fields):
        
        if not email:
            raise ValueError(_('You must provide an email address'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name,
                          **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
             
class Users(AbstractBaseUser):
    class Meta:
        verbose_name_plural = 'Users'
    
    email = models.EmailField(_('email'), max_length=100, unique=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    profession = models.CharField(max_length=50, blank=True)
    institution = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    is_superuser = models.BooleanField(_('Superuser status'), default=False, help_text=_('Designates that this user has all permissions without explicitly assigning them.'))
    is_staff = models.BooleanField(_('Staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('Active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    
    objects = CustomAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return True
     
class Studies(models.Model):
    class Meta:
        verbose_name = 'Study (Any Group)'
        verbose_name_plural = 'Studies (Any Group)'

    Unique_identifier = models.CharField(max_length=20, null=True, blank=True, verbose_name='Unique Identifier', help_text='Internal use only')    
    STUDY_GROUPS = (
        ('SST', 'Superficial skin and throat'),
        ('IG', 'Invasive GAS'),
        ('ARF', 'ARF'),
        ('ASPGN', 'APSGN'),                   
    )
    Study_group = models.CharField(max_length=5, choices=STUDY_GROUPS, blank=True, verbose_name='Study Group')
    Paper_title = models.CharField(max_length=200, verbose_name='Paper Title')
    Paper_link = models.CharField(max_length=200, blank=True, verbose_name='Link to Paper Download')

    Year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)], null=True, blank=True, verbose_name='Publication Year')

    Disease = models.CharField(max_length=60, blank=True)
    STUDY_DESIGNS = (
        ('CS', 'Case series'),
        ('CST', 'Cross-sectional'),
        ('P', 'Prospective'),
        ('PRP', 'Prospective and Retrospective'),
        ('PC', 'Prospective cohort'),
        ('R', 'Report'),
        ('RP', 'Retrospective'),  
        ('RPR', 'Retrospective review'), 
        ('RPC', 'Retrospective cohort'),  
        ('RA', 'Review article'),              
        ('O', 'Other'),        
    )
    Study_design = models.CharField(max_length=3, choices=STUDY_DESIGNS)
    Study_design_other = models.CharField(max_length=200, blank=True, default='')
    Study_description = models.CharField(max_length=200, blank=True, default='')
    Case_definition = models.CharField(max_length=200, blank=True, default='')
    Case_findings = models.CharField(max_length=200, blank=True, default='')
    Case_findings_other = models.CharField(max_length=200, blank=True, default='')
    Case_cap_meth = models.CharField(max_length=200, blank=True, default='')
    Case_cap_meth_other = models.CharField(max_length=200, blank=True, default='')

    Data_source = models.CharField(max_length=200, blank=True, default='')
    Coverage = models.CharField(max_length=200, blank=True, default='')

    Jurisdiction = models.CharField(max_length=200, blank=True, default='')
    Specific_region = models.CharField(max_length=200, blank=True, default='')
    Climate = models.CharField(max_length=200, blank=True, default='')
    Aria_remote = models.CharField(max_length=200, blank=True, default='')

    Population_group_strata = models.CharField(max_length=200, blank=True, default='')
    Population_denom = models.CharField(max_length=200, blank=True, default='')

    AGE_GROUPS = (
        ('ALL', 'All'),
        ('AD', 'Adults'),
        ('C', 'Children'),
        ('AL', 'Adolescents'),
        ('EA', 'Elderly Adults'),
    )
    Age_general = models.CharField(max_length=5, choices=AGE_GROUPS, blank=True, verbose_name='Age Category')

    Age_min = models.DecimalField(validators=[MaxValueValidator(150.0)],decimal_places=2, max_digits=5, null=True, blank=True)
    Age_max = models.DecimalField(validators=[MaxValueValidator(150.0)],decimal_places=2, max_digits=5, null=True, blank=True)
    Age_original = models.CharField(max_length=200, blank=True, verbose_name='Age Category (Original)')

    Burden_measure = models.CharField(max_length=200, blank=True)

    Ses_reported = models.BooleanField(null=True, blank=True)
    Mortality_data = models.BooleanField(null=True, blank=True)
    Method_limitations = models.BooleanField(null=True, blank=True)

    Limitations_identified = models.CharField(max_length=200, blank=True)
    Other_points = models.CharField(max_length=200, blank=True)
    Notes = models.TextField(blank=True, default='')

    # For approving the adding of studies
    is_approved = models.BooleanField(default=False, verbose_name='Study Approved', blank=False, help_text=_('Designates whether this study has been approved or is pending approval.'))
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Study Added By User')
    
    def get_flags(self):
        return (
            {'field': field, 'value': getattr(self, field.name)}
            for field in self._meta.get_fields()
            if isinstance(field, models.BooleanField) #and getattr(self, field.name) is not None
        )

    def __str__(self):
        return "%s (%s)" % (self.Paper_title, self.Year)

# LH: Rough draft for Results model. Needs further work with cleaner database. Some fields may be redundant upon cleanup.  
class Results(models.Model):
    class Meta:
        verbose_name = 'Result (Any Group)'
        verbose_name_plural = 'Results (Any Group)'

    Study = models.ForeignKey(Studies, on_delete=models.CASCADE, null=True, blank=True)
    AGE_GROUPS = (
        ('ALL', 'All ages'),
        ('AD', 'Adult'),
        ('C', 'Children'),
        ('AL', 'Adolescents'),
        ('I', 'Infant'),
        ('M', 'Mix'),
    )
    Age_general = models.CharField(max_length=5, choices=AGE_GROUPS, blank=True, verbose_name='Age Category')

    Age_min = models.DecimalField(validators=[MaxValueValidator(150.0)],decimal_places=2, max_digits=5, null=True, blank=True, verbose_name='Minimum Age (years)')
    Age_max = models.DecimalField(validators=[MaxValueValidator(150.0)],decimal_places=2, max_digits=5, null=True, blank=True, verbose_name='Maximum Age (years)')

    Age_original = models.CharField(max_length=50, blank=True, verbose_name='Age Category (Original)')
    Population_gender = models.CharField(max_length=30, blank=True)
    Indigenous_status = models.CharField(max_length=20, blank=True, default='')
    Indigenous_population = models.CharField(max_length=30, blank=True, default='')
    Country = models.CharField(max_length=30, blank=True, default='')
    Jurisdiction = models.CharField(max_length=30, blank=True, default='')
    Specific_location = models.CharField(max_length=100, blank=True, default='')

    Year_start = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)], null=True, blank=True)
    Year_stop = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)], null=True, blank=True)

    Observation_time_years = models.DecimalField(validators=[MaxValueValidator(150.0)],decimal_places=2, max_digits=5, null=True, blank=True)

    Numerator = models.PositiveIntegerField(null=True, blank=True)
    Denominator = models.PositiveIntegerField(null=True, blank=True)  

    Point_estimate = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    Point_estimate_original = models.CharField(max_length=30, blank=True, default='')  # some fields have non-numeric values like "14% (8)" or other weird things

    Measure = models.TextField(blank=True, default='')

    BOOL_CHOICE = (
        ('Y', 'Yes'),
        ('N', 'No'),
        ('?', 'N/A'),
    )    
    Interpolated_from_graph = models.CharField(max_length=1, choices=BOOL_CHOICE, blank=True, default='')
    Age_standardisation	= models.CharField(max_length=1, choices=BOOL_CHOICE, blank=True, default='')
    Dataset_name = 	models.CharField(max_length=1, choices=BOOL_CHOICE, blank=True, default='')
    Proportion = models.CharField(max_length=1, choices=BOOL_CHOICE, blank=True, default='')
    Mortality_flag = models.CharField(max_length=1, choices=BOOL_CHOICE, blank=True, default='')
    Recurrent_ARF_flag = models.CharField(max_length=1, choices=BOOL_CHOICE, blank=True, default='')
    GAS_attributable_fraction = models.CharField(max_length=1, choices=BOOL_CHOICE, blank=True, default='')
    Defined_ARF	= models.CharField(max_length=1, choices=BOOL_CHOICE, blank=True, default='')

    BOOL_CHOICE_FIELDS = ('Interpolated_from_graph', 'Age_standardisation', 'Dataset_name', 
        'Proportion', 'Mortality_flag', 'Recurrent_ARF_flag', 'GAS_attributable_fraction', 'Defined_ARF')

    Focus_of_study = models.TextField(blank=True, default='')
    Notes = models.TextField(blank=True, default='')

    # For approving the adding of results
    is_approved = models.BooleanField(default=False, verbose_name='Results Approved', blank=False, help_text=_('Designates whether this study has been approved or is pending approval.'))
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Results Added By User')
    
    def get_burden(self):
        if self.Point_estimate is not None:
            return "%0.2f%%" % self.Point_estimate
        elif self.Numerator is not None and self.Denominator is not None:
            return "%d/%d" % (self.Numerator, self.Denominator)
        elif self.Numerator is None and self.Denominator is None and self.Point_estimate is None:
            return self.Point_estimate_original
        else:
            return 'Unknown'

    def get_flags(self):
        # return array of flags for displaying in 2 columns
        flags = []
        prev = None
        for bool_field in self.BOOL_CHOICE_FIELDS:
            field = self._meta.get_field(bool_field)
            value = getattr(self, bool_field)
            if not (value == 'Y' or value == 'N'):
                continue

            flags.append({
                'field': field,
                'value': value,
            })
        return flags

    def __str__(self):
        if not self.Study:
            return "Burden: %s" % (self.get_burden(), )
        return '%s (Burden: %s)' % (self.Study.Paper_title, self.get_burden())

class ProxyManager(models.Manager):
    filter_args = None
    def __init__(self, filter_args=None):
        self.filter_args = filter_args or {}
        super().__init__()
    
    def get_queryset(self):
        return super().get_queryset().filter(**self.filter_args)

proxies = []
def proxy_model_factory(model, verbose_name, **filter_args):
    global proxies
    name = '_'.join('%s.%s' % (k.replace('_', ''), v) for k, v in filter_args.items()) + '_' + model._meta.model_name

    meta = type('Meta', (), {
        'proxy': True,
        'verbose_name': verbose_name,
        'verbose_name_plural': verbose_name,
    })

    cls = type(name, (model, ), {
        '__module__': __name__,
        'Meta': meta,
        'objects': ProxyManager(filter_args=filter_args),
    })

    proxies.append(cls)

    return cls

ARFResults = proxy_model_factory(Results, 'ARF Results', Study__Study_group='ARF')
ARFStudies = proxy_model_factory(Studies, 'ARF Studies', Study_group='ARF')

ASPGNResults = proxy_model_factory(Results, 'ASPGN Results', Study__Study_group='ASPGN')
ASPGNStudies = proxy_model_factory(Studies, 'ASPGN Studies', Study_group='ASPGN')

IGResults = proxy_model_factory(Results, 'Invasive GAS Results', Study__Study_group='IG')
IGStudies = proxy_model_factory(Studies, 'Invasive GAS Studies', Study_group='IG')

SSTResults = proxy_model_factory(Results, 'Superficial Skin & Throat Results', Study__Study_group='SST')
SSTStudies = proxy_model_factory(Studies, 'Superficial Skin & Throat Studies', Study_group='SST')

# one way to possibly add admin page approval function
#UnapprovedResults = proxy_model_factory(Results, 'Results (Pending Approval)', Is_approved=False)

is_approved_proxies = []
def is_approved_proxy_model_factory(model, verbose_name, **filter_args):
    global is_approved_proxies
    name = '_'.join('%s_%s' % (k.replace('_', ''), v) for k, v in filter_args.items()) + '_' + model._meta.model_name

    meta = type('Meta', (), {
        'proxy': True,
        'verbose_name': verbose_name,
        'verbose_name_plural': verbose_name,
    })

    cls = type(name, (model, ), {
        '__module__': __name__,
        'Meta': meta,
        'objects': ProxyManager(filter_args=filter_args),
    })

    is_approved_proxies.append(cls)

    return cls

UnapprovedStudies = is_approved_proxy_model_factory(Studies, 'Studies (Pending Approval)', is_approved=False)
UnapprovedResults = is_approved_proxy_model_factory(Results, 'Results (Pending Approval)', is_approved=False)