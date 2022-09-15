from django.core.management.base import BaseCommand, CommandError

import csv
import logging

from django.db import transaction
from django.db.models import fields
from django.core.exceptions import FieldDoesNotExist
from database.models import Studies, Results

logger = logging.getLogger(__name__)

NULL_VALUES = ('n/a', 'not applicable', '')
TRUE_VALUES = ('t', '1', 'yes', 'y')
FALSE_VALUES = ('f', '0', 'no', 'n')

def parse_bool(value):
    if value is None:
        return None

    value = value.lower()
    if value in TRUE_VALUES:
        return True
    if value in FALSE_VALUES:
        return False
    else:
        return None

def format_bool_charfield(value):
    if value is None:
        return '?'
    if value == True:
        return 'Y'
    else:
        return 'F'

def parse_django_field_value(model, field, value):
    try:
        djfield = model._meta.get_field(field)

        if isinstance(djfield, (fields.CharField, fields.TextField)):
            return value or ''

        if value.lower() in NULL_VALUES:
            return None
        elif isinstance(djfield, fields.DecimalField):
            value = float(value)
        elif isinstance(djfield, (fields.PositiveSmallIntegerField, fields.PositiveIntegerField)):
            value = int(value)
        elif isinstance(djfield, fields.BooleanField):
            value = parse_bool(value)
        else:
            return value
            
    except (ValueError, AttributeError):
        logger.error('%s: bad field value "%s" for field "%s"' % (
            model._meta.model_name, value, field
        ))
    except FieldDoesNotExist:
        logger.error('%s: field "%s" does not exist' % (model._meta.model_name, field))

class Command(BaseCommand):
    help = 'Import a Rezdy Pickup Manifest (CSV file) to the database'

    def add_arguments(self, parser):
        parser.add_argument('studies_csv', help='CSV file containing studies data')
        parser.add_argument('results_csv', help='CSV file containing results data')
        
    def handle(self, *args, **options):
        if not (studies_csv := open(options['studies_csv'], 'r')):
            raise CommandError('Cannot open Studies CSV file at "%s"' % options['studies_csv'])
        if not (results_csv := open(options['results_csv'], 'r')):
            raise CommandError('Cannot open Results CSV file at "%s"' % options['results_csv'])

        # import studies first
        reader = csv.DictReader(studies_csv)
        with transaction.atomic():
            Studies.objects.all().delete()
            for row in reader:
                study = Studies()
                #fields = ('Age_general', 'Age_min', 'Age_max', 'Age_original', 'Population_gender', 'Indigenous_status', 'Indigenous_population')
                for field, value in row.items():
                    value = parse_django_field_value(Studies, field, value)
                    setattr(study, field, value)

                study.save()

        # then results
        reader = csv.DictReader(results_csv)
        with transaction.atomic():
            Results.objects.all().delete()
            for row in reader:
                result = Results()
                for field, value in row.items():
                    if field in ('Results_ID', 'Result_group'):
                        continue
                    value = parse_django_field_value(Results, field, value)
                    if field in Results.BOOL_CHOICE_FIELDS:
                        value = format_bool_charfield(parse_bool(value))
                    setattr(result, field, value)
                studies = list(Studies.objects.filter(Unique_identifier=row['Results_ID']))
                if len(studies) == 0:
                    logger.error('No study found with ID "%s", skipping import' % row['Results_ID'])
                    continue
                elif len(studies) > 1:
                    logger.error('Multiple studies found with id "%s"' % row['Results_ID'])
                    result.Study = studies[0]
                else:
                    result.Study = studies[0]

                result.save()