from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.

class CustomAccountManager(BaseUserManager):
    
    def create_superuser(self, email, username, password, **other_fields):
    
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        
        if other_fields.get('is_admin') is not True:
            raise ValueError(
                'Superuser must be assigned to is_admin=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_user(self, email, username, password, **other_fields):
        
        if not email:
            raise ValueError(_('You must provide an email address'))
        if not username:
            raise ValueError(_('You must provide a user name.'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
        
class Users(AbstractBaseUser):

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    email = models.EmailField(_('email'), max_length=100, unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    profession = models.CharField(max_length=50, blank=True)
    institution = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = CustomAccountManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return True
    
class Studies(models.Model):
    class Meta:
        verbose_name = 'Study'
        verbose_name_plural = 'Studies'

    Unique_identifier = models.CharField(max_length=20)    
    STUDY_GROUPS = (
        ('SST', 'Superficial skin and throat'),
        ('IG', 'Invasive GAS'),
        ('ARF', 'ARF'),
        ('ASPGN', 'APSGN'),                   
    )
    Study_group = models.CharField(max_length=5, choices=STUDY_GROUPS)
    
    Paper_title = models.CharField(max_length=200)
    Paper_link = models.CharField(max_length=200)
    Year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    Disease = models.CharField(max_length=60)
    STUDY_DESIGNS = (
        ('CST', 'Cross-sectional'),
        ('P', 'Prospective'),
        ('RP', 'Retrospective'),
        ('PRP', 'Prospective and Retrospective'),
        ('CS', 'Case series'),
        ('R', 'Report'),
        ('PC', 'Prospective cohort'),
        ('RPR', 'Retrospective review'),
        ('RA', 'Review article'), 
        ('RPC', 'Retrospective cohort'),
        ('O', 'Other'),        
    )
    Study_design = models.CharField(max_length=3, choices=STUDY_DESIGNS)
    Study_design_other = models.CharField(max_length=200)
    Study_description = models.CharField(max_length=200)
    Case_definition = models.CharField(max_length=200)
    Case_findings = models.CharField(max_length=200)
    Case_findings_other = models.CharField(max_length=200)
    Data_source = models.CharField(max_length=200)
    Case_cap_meth = models.CharField(max_length=200)
    Case_cap_meth_other = models.CharField(max_length=200)
    Coverage = models.CharField(max_length=200)
    Jurisdiction = models.CharField(max_length=200)
    Specific_region = models.CharField(max_length=200)
    Climate = models.CharField(max_length=200)
    Aria_remote = models.CharField(max_length=200)
    Population_group_strata = models.CharField(max_length=200)
    Population_denom = models.CharField(max_length=200)
    Age_original = models.CharField(max_length=200)
    AGE_GROUPS = (
        ('ALL', 'All'),
        ('AD', 'Adults'),
        ('C', 'Children'),
        ('AL', 'Adolescents'),
        ('EA', 'Elderly Adults'),
    )
    Age_general = models.CharField(max_length=5, choices=AGE_GROUPS)
    Age_min = models.DecimalField(validators=[MaxValueValidator(150.0)],decimal_places=2, max_digits=5)
    Age_max = models.DecimalField(validators=[MaxValueValidator(150.0)],decimal_places=2, max_digits=5)
    Burden_measure = models.CharField(max_length=200)
    Ses_reported = models.BooleanField()
    Mortality_data = models.BooleanField()
    Method_limitations = models.BooleanField()    
    Limitations_identified = models.CharField(max_length=200)
    Other_points = models.CharField(max_length=200)

# FVP: placeholder Results model to test the admin site with. Not intended to be the final product!
class Results(models.Model):
    class Meta:
        verbose_name_plural = 'Results'

    study = models.ForeignKey(Studies, on_delete=models.CASCADE, )
    year_start = models.PositiveIntegerField()
    year_stop = models.PositiveIntegerField()
    ages = models.CharField(max_length=100, blank=True)
    point_estimate = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    numerator = models.PositiveIntegerField(null=True, blank=True)
    denominator = models.PositiveIntegerField(null=True, blank=True)
    measure = models.TextField(blank=True)
    
    def __str__(self):
        if self.point_estimate:
            return "%s: %0.2f%%" % (self.study, self.point_estimate)
        else:
            return "%s: %d/%d" % (self.study, self.numerator, self.denominator)
    # etc