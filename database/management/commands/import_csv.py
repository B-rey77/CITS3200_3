from django.core.management.base import BaseCommand, CommandError

import logging
from database.importer import import_methods_results

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import a Rezdy Pickup Manifest (CSV file) to the database'

    def add_arguments(self, parser):
        parser.add_argument('studies_csv', help='CSV file containing studies data')
        parser.add_argument('results_csv', help='CSV file containing results data')
        
    def handle(self, *args, **options):
        if not (studies_csv := open(options['studies_csv'], 'r', errors='replace')):
            raise CommandError('Cannot open Studies CSV file at "%s"' % options['studies_csv'])
        if not (results_csv := open(options['results_csv'], 'r', errors='replace')):
            raise CommandError('Cannot open Results CSV file at "%s"' % options['results_csv'])

        errors = import_methods_results(studies_csv, results_csv)
        
        