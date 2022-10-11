import csv
import logging

from django.db import transaction
from django.db.models import fields
from django.core.exceptions import FieldDoesNotExist
from database.models import Studies, Results
import decimal

logger = logging.getLogger(__name__)

NULL_VALUES = ('n/a', 'not applicable', 'none', 'not defined')
TRUE_VALUES = ('t', '1', 'yes', 'y', 'true')
FALSE_VALUES = ('f', '0', 'no', 'n', 'false')

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
            if djfield.choices:
                for c in djfield.choices:
                    if value.lower() == c[1].lower() or value.lower() == c[0].lower():
                        return (c[0], True)
                return ('Value "%s" not available for choice field %s' % (value, field), False)
            return (value or '', True)

        if value.lower() in NULL_VALUES:
            return (None, True)
        elif isinstance(djfield, fields.DecimalField):
            value = float(value)
            if djfield.decimal_places:
                value = round(value, djfield.decimal_places)
            if djfield.max_digits:
                digits = djfield.max_digits - (djfield.decimal_places or 0)
                value = min(value, pow(10, digits) - 1)
        elif isinstance(djfield, (fields.PositiveSmallIntegerField, fields.PositiveIntegerField)):
            value = int(value.replace(',', ''))
        elif isinstance(djfield, fields.BooleanField):
            value = parse_bool(value)
        else:
            pass

        return value, True
            
    except (ValueError, AttributeError, decimal.InvalidOperation):
        return '%s: bad field value "%s" for field "%s"' % (
            model._meta.model_name, value, field
        ), False
    except FieldDoesNotExist:
        return '%s: field "%s" does not exist' % (model._meta.model_name, field), False

def import_methods_results(studies_csv, results_csv):
    # import studies first
    all_errors = []

    reader = csv.DictReader(studies_csv)
    
    with transaction.atomic():
        Studies.objects.all().delete()
        n = 1
        for row in reader:
            if not 'Unique_identifier' in row:
                return ['Could not find Unique_identifier field in Studies CSV file']
            
            n += 1
            study = Studies()
            row_errors = []
            #fields = ('Age_general', 'Age_min', 'Age_max', 'Age_original', 'Population_gender', 'Indigenous_status', 'Indigenous_population')
            for field, value in row.items():
                if field == 'SES_reported':
                    field = 'Ses_reported'
                elif field == 'Data_source__if_applicable_':
                    field = 'Data_source'
                
                value, ok = parse_django_field_value(Studies, field, value)
                if not ok:
                    row_errors.append(value)
                else:
                    setattr(study, field, value)
            if len(row_errors) > 0:
                logger.error('Study id %s has data inconsistencies: %s' % (study.Unique_identifier, ', '.join(row_errors)))
                study.Notes += '\nData Inconsistencies Detected:\n' + '\n'.join(row_errors)
                all_errors.append('Studies/Methods row %d is inconsistent: %s' % (n, ', '.join(row_errors)))

            if not 'is_approved' in row:
                study.is_approved = True
            study.save()

    # then results
    reader = csv.DictReader(results_csv)
    with transaction.atomic():
        Results.objects.all().delete()
        n = 1
        for row in reader:
            n += 1
            result = Results()
            row_errors = []
            for field, value in row.items():
                if field in ('Results_ID', 'Result_group'):
                    continue
                
                if field == 'Data_source__if_applicable_':
                    field = 'Data_source'
                
                parsed_value, ok = parse_django_field_value(Results, field, value)

                if not ok:
                    logger.error("Results: row %d: can't parse value '%s' for field %s" % (n, value, field))
                    row_errors.append("Couldn't parse value '%s' for field %s" % (value, field))
                else:
                    setattr(result, field, parsed_value)

            studies = list(Studies.objects.filter(Unique_identifier=row['Results_ID']))

            if len(studies) == 0:
                logger.error('Results: No study found with ID "%s"' % row['Results_ID'])
                row_errors.append('No matching study found with Study ID %s in group %s' % (row['Results_ID'], row['Result_group']))

            elif len(studies) > 1:
                logger.error('Multiple studies found with id "%s"' % row['Results_ID'])
                result.Study = studies[0]
                row_errors.append('Multiple studies match Study ID %s\n' % row['Results_ID'])
            else:
                result.Study = studies[0]

            if len(row_errors) > 0:
                result.Notes += '\nData Inconsistencies Detected:\n' + '\n'.join(row_errors)
                all_errors.append('Results row %d is inconsistent: %s' % (n, ', '.join(row_errors)))
            if not 'is_approved' in row:
                result.is_approved = True
            result.save()
    return all_errors