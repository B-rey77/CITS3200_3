from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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
    about = models.TextField(_('about'), max_length=500, blank=True)
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
    
# FVP: set up some placeholder models to test the admin site with. Not intended to be the final product!
class Study(models.Model):
    class Meta:
        verbose_name = 'Study'
        verbose_name_plural = 'Studies'

    title = models.CharField(max_length=1000)
    identifier = models.CharField(max_length=20) # unique identifier as in the spreadsheet
    pub_year = models.PositiveIntegerField()
    # etc.

    def __str__(self):
        return "%s (%04d)" % (self.title, self.pub_year)

class Results(models.Model):
    class Meta:
        verbose_name_plural = 'Results'

    study = models.ForeignKey(Study, on_delete=models.CASCADE, )
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