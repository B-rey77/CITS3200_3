from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib import admin

BOOL_CHOICE = (
        ('Y', 'Yes'),
        ('N', 'No'),
        ('?', 'N/A'),
) 

AGE_GROUPS = (
        ('ALL', 'All'),
        ('AD', 'Adult'),
        ('C', 'Children'),
        ('AL', 'Adolescents'),
        ('EA', 'Elderly Adults'),
        ('I', 'Infant'),
        ('M', 'Mix'),
        ('N/A', 'N/A')
)

STUDY_GROUPS = (
        ('SST', 'Superficial skin and throat'),
        ('IG', 'Invasive GAS'),
        ('ARF', 'ARF'),
        ('ASPGN', 'APSGN'),                   
)


# Create your models here.

class CustomAccountManager(BaseUserManager):
    
    def create_superuser(self, email, first_name, last_name, password, **other_fields):
    
        other_fields.setdefault('is_superuser', True)
        
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

    STUDY_GROUPS = (
        ('SST', 'Superficial skin and throat'),
        ('IG', 'Invasive GAS'),
        ('ARF', 'ARF'),
        ('ASPGN', 'APSGN'),                   
    )
    Study_group = models.CharField(max_length=5, choices=STUDY_GROUPS, blank=True, verbose_name='Study Group',
    help_text='Broad classification of the Strep A-associated disease type that the study was based on: (i) Superficial skin and/or throat infections, (ii) Invasive Strep A infections, (iii) Acute Rheumatic Fever (ARF), (iv) Acute Post Streptococcal Glomerulonephritis (APSGN).')
    
    Study_description = models.CharField(max_length=200, blank=True, default='', help_text='Name of the first author, abbreviated name of journal and year of manuscript publication. Example: McDonald, Clin Infect Dis, 2006')
    
    Paper_title = models.CharField(max_length=200, verbose_name='Paper Title', help_text='Title of the published manuscript/report.')
    
    Paper_link = models.CharField(max_length=200, blank=True, verbose_name='Link to Paper Download',
    help_text='URL or doi to facilitate access to the source manuscript/report, full access will depend on open/institutional access permissions set by each journal.')
    
    Unique_identifier = models.CharField(max_length=8, null=True, blank=True, verbose_name='Unique Identifier',
    help_text='Links the methods dataset to the results dataset, which contains estimates reported by the same study (often multiple results per study). Each Unique Identifier consists of the year of publication followed by the first four letters of the first author. Example: 2006MCDO is a unique identifier for McDonald, Clin Infect Dis, 2006, which provides a link between the methods used by 2006MCDO to obtain the 21 estimates reported in that manuscript. ') 
    
    Year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)], null=True, blank=True, verbose_name='Publication Year',
    help_text='Year of publication of manuscript/report.')
  
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
    Study_design = models.CharField(max_length=3, choices=STUDY_DESIGNS,
    help_text='Study classification based on the temporality of data collection. Prospective (if study involves screening or active surveillance or primary data collection) or retrospective (study involves using either administrative/medical record data from hospitals, primary health centres, laboratory or population datasets) or both prospective and retrospective (if study has both components). Other categories which are rarely used include report and outbreak investigation.')
    
    Study_design_temporality = models.CharField(max_length=200, blank=True, default='', verbose_name='Study design (with respect to temporality)', 
    help_text='Study classification based on the temporality of data collection. Prospective (if study involves screening or active surveillance or primary data collection) or retrospective (study involves using either administrative/medical record data from hospitals, primary health centres, laboratory or population datasets) or both prospective and retrospective (if study has both components). Other categories which are rarely used include report and outbreak investigation.')
    
    Case_finding_meth= models.CharField(max_length=200, blank=True, default='',verbose_name='Case finding method',
    help_text='Method of case identification, for example: screening or active surveillance for reporting cases of impetigo or skin sores; population registers for ARF; medical record review.') 
    
    Case_definition_meth = models.CharField(max_length=200, blank=True, default='', verbose_name='Case definition method',
    help_text='Indicates the process used to identify Strep A-associated diseases, such as: notifications, ICD codes, Snowmed/ICPC codes, clinical diagnosis, laboratory diagnosis, echocardiography or combined methods.   ')

    Data_source = models.CharField(max_length=200, blank=True, default='', verbose_name='Data source (if applicable', 
    help_text='Name of the dataset, project, consortium or specific disease register. ')
    
    Coverage = models.CharField(max_length=200, blank=True, default='', verbose_name='Geographic Coverage', 
    help_text='Level of geographic coverage in the study, categorised as (i) national/multli-jurisdictional, (ii) state, (iii) subnational/ regional, (iv) single institution/ service.  ')

    Jurisdiction = models.CharField(max_length=200, blank=True, default='', 
    help_text='Jurisdictional location of the study, categorized by individual jurisdiction name (WA, NT, SA, QLD, NSW, Vic) or combination of jurisdictions (Combination – Northern Australia or Combination- others). ')
    
    Specific_region = models.CharField(max_length=200, blank=True, default='', verbose_name='Specific region (if applicable)', 
    help_text='Specific region covered by the study, for example: city / town if the study involved a single institution / service; or number and location of remote communities included. ')
    
    Climate = models.CharField(max_length=200, blank=True, default='',
    help_text='Climatic conditions based on the geographic coverage of studies, for example: “Tropical” for studies conducted at the Top-End NT, “Temperate” for studies from Victoria or NSW. ')
    
    Aria_remote = models.CharField(max_length=200, blank=True, default='', verbose_name='Remoteness',
    help_text='Classification into metropolitan, regional and remote areas based on the ARIA+ (Accessibility and Remoteness Index of Australia) system.')

    Population_group_strata = models.CharField(max_length=200, blank=True, default='', 
    help_text='Indicates whether burden estimates were presented stratified by population group or not i.e.) Yes – then Indigenous vs. non-Indigenous results are presented, No – general population burden estimates only with no stratification.')
    
    Population_denom = models.CharField(max_length=200, blank=True, default='', verbose_name='Population denominator',
    help_text='The population used as the denominator by the study, for example: general population, Indigenous population, hospitalised patients.')

    Age_original = models.CharField(max_length=200, blank=True, verbose_name='Age Category')
    Age_general = models.CharField(max_length=200, blank=True, verbose_name='Age Category (General)')
    Age_min = models.DecimalField(validators=[MaxValueValidator(150.0)],decimal_places=2, max_digits=5, null=True, blank=True, verbose_name='Minimum age (years)')
    Age_max = models.DecimalField(validators=[MaxValueValidator(150.0)],decimal_places=2, max_digits=5, null=True, blank=True, verbose_name='Maximum age (years)')

    Burden_measure = models.CharField(max_length=200, blank=True,
    help_text='The epidemiological measure presented as a point estimate by the study. The categories include: population incidence, population prevalence or proportion (not population based).')

    Ses_reported = models.BooleanField(null=True, blank=True, verbose_name='Socioeconomic status (SES) reported',
    help_text='This variable indicates “Yes/No”, whether socioeconomic status is reported by the study.')

    Mortality_data = models.BooleanField(null=True, blank=True, verbose_name='Mortality',
    help_text='This variable indicates “Yes/No”, whether mortality estimates are reported by the study.')

    Method_limitations = models.BooleanField(null=True, blank=True,
    help_text='This variable briefly describes whether method limitations were specified by the authors of the publication.')

    Limitations_identified = models.CharField(max_length=200, blank=True)
    Other_points = models.TextField(blank=True, default='',
    help_text='This variable captures any other relevant notes relating to the study that may impact the interpretation of Strep A burden estimates.')
    
   

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
    
    Study = models.ForeignKey(Studies, on_delete=models.CASCADE)

    Age_general = models.CharField(max_length=50, blank=True, verbose_name='Age Category (General)', 
    help_text='The general age grouping considered for inclusion by the study, classified as “all ages” (if studies did not have any age restrictions); “infants”, “young children”, “children and adolescents”, “18 years and younger” and “16 years and older”. ')
    
    Age_min = models.DecimalField(validators=[MaxValueValidator(150.0)],decimal_places=2, max_digits=5, null=True, blank=True, verbose_name='Minimum Age (years)')
    
    Age_max = models.DecimalField(validators=[MaxValueValidator(150.0)],decimal_places=2, max_digits=5, null=True, blank=True, verbose_name='Maximum Age (years)')
    Age_original = models.CharField(max_length=50, blank=True, verbose_name='Age Category (Original)')
    
    Population_gender = models.CharField(max_length=30, blank=True, verbose_name='Population - Gender',
    help_text='This variable captures stratification by sex (where reported), with categories of “males”, “females”, “males and females”. ')
    
    Indigenous_status = models.CharField(max_length=20, blank=True, default='', verbose_name='Population - Indigenous Status',
    help_text='This variable captures stratification by Indigenous status, with categories of “general population”, “Indigenous” and “non-Indigenous”. ')
    
    Indigenous_population = models.CharField(max_length=30, blank=True, default='',
    help_text='This variable captures stratification of the Indigenous population (where reported) into “Aboriginal”, “Torres Strait Islander” or “both Aboriginal and Torres Strait Islanders”. ')
    
    Country = models.CharField(max_length=30, blank=True, default='',
    help_text='Country where study was conducted (for future use, in the case that international studies are added to the data collection).')

    Jurisdiction = models.CharField(max_length=30, blank=True, default='',
    help_text='Jurisdictional location of the study, categorized by individual jurisdiction name (WA, NT, SA, QLD, NSW, Vic) or combination of jurisdictions (Combination – Northern Australia or Combination- others). ')
    
    Specific_location = models.CharField(max_length=100, blank=True, default='', verbose_name='Specific geographic locations',
    help_text='Point estimates stratified by specific geographic locations (where reported), for example: Kimberley, Far North Queensland or Central Australia.')
    
    Year_start = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)], null=True, blank=True,
    help_text='Start year for the observed point estimates within the study, allowing for temporal mapping of the point estimates. ')
    
    Year_stop = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)], null=True, blank=True,
    help_text='End year for the observed point estimates within the study, allowing for temporal mapping of the point estimates. ')
    
    Observation_time_years = models.DecimalField(validators=[MaxValueValidator(150.0)],decimal_places=2, max_digits=5, null=True, blank=True, verbose_name='Observational period,',
    help_text='Total observation time used by the study for generating the point estimate. ')
    
    Numerator = models.PositiveIntegerField(null=True, blank=True,
    help_text='This variable reports the numerators for studies reporting point estimates as proportions (non-population based). ')
    
    Denominator = models.PositiveIntegerField(null=True, blank=True,
    help_text='This variable reports the denominators for studies reporting point estimates as proportions (non-population based). ')  
    
    Point_estimate = models.CharField(null=True, blank=True, max_length=100,
    help_text='Must be interpreted together with Measure to provide the point estimate reported by the study within the correct measurement context. For example: 2020KATZ reports a point estimate of “4.6” and measure of “per 100,000 population”.  ')
    
    Measure = models.TextField(blank=True, default='') 
    
    Interpolated_from_graph = models.BooleanField(null=True, blank=True,
    help_text='Indicator variable which is “Yes” if point estimate is interpolated and “No” or “Unknown” otherwise.')
    
    Age_standardisation	= models.BooleanField(null=True, blank=True,
    help_text='Indicator variable which is “Yes” if point estimate is age-standardised and “No” or “Unknown” otherwise.')
    
    Dataset_name = models.BooleanField(null=True, blank=True, help_text='Empty variable')

    Proportion = models.BooleanField(null=True, blank=True,
    help_text='Indicator variable which is “Yes” if point estimate is a proportion and “No” or “Unknown” otherwise.')

    Mortality_flag = models.BooleanField(null=True, blank=True,
    help_text='Indicator variable which is “Yes” if point estimate is a mortality estimate and “No” or “Unknown” otherwise.')
    
    Recurrent_ARF_flag = models.BooleanField(null=True, blank=True,
    help_text='Indicator variable which is “Yes” if point estimate includes recurrent ARF and “No” or “Unknown” otherwise (applicable to ARF burden estimates only).')
    
    GAS_attributable_fraction = models.BooleanField(null=True, blank=True,
    help_text='Indicator variable which is “Yes” if point estimate is a proportion which is GAS-specific and therefore represents a GAS-attributable fraction and “No” or “Unknown” otherwise.')
    
    Defined_ARF	= models.BooleanField(null=True, blank=True,
    help_text='Indicator variable which is “Yes” if point estimate has defined ARF and “No” or “Unknown” otherwise.')

    Focus_of_study = models.CharField(max_length=200,blank=True, default='',
    help_text='Short sentence which summarises the focus of the study, to assist with interpreting the burden estimate.')

    BOOL_CHOICE_FIELDS = ('Interpolated_from_graph', 'Age_standardisation', 'Dataset_name', 
        'Proportion', 'Mortality_flag', 'Recurrent_ARF_flag', 'GAS_attributable_fraction', 'Defined_ARF')

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