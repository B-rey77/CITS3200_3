from django.core.management.base import BaseCommand, CommandError

import csv

from django.db import transaction
from database.models import Studies, Results

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
            for row in reader:
                study = Studies()
                for field, value in row.items():
                    setattr(study, field, value)
                study.save()

        # then results
        reader = csv.DictReader(results_csv)
        with transaction.atomic():
            for row in reader:
                result = Results()
                for field, value in row.items():
                    setattr(result, field, value)

                result.Study = Studies.objects.get(Unique_identifier=row['Results_ID'])
                result.save()