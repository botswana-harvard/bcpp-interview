import csv
import os

from django.apps import apps as django_apps
from django.core.management.base import BaseCommand, CommandError
from bcpp_interview.models import PotentialSubject
from django.db.utils import IntegrityError


class Command(BaseCommand):

    """Import model data from CSV.

    For example:
        python manage.py load_locator_data bcpp_interview.subjectlocator /Users/erikvw/Documents/bcpp/qualitative_substudy/qualitative_substudy_subject_locators.csv

        python manage.py load_locator_data bcpp_interview.subjectlocator /home/django/qualitative_substudy_subject_locators.csv
    """

    help = 'Load CSV data into a model if PotentialSubject exists (e.g. locator)'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help='A model\'s app_label.model_name')
        parser.add_argument('csv_filename', type=str, help='Full path to CSV file')

    def handle(self, *args, **options):
        csv_filename = options['csv_filename']
        if not os.path.exists(csv_filename):
            raise CommandError('CSV file does not exist. Got {}'.format(csv_filename))
        try:
            app_label, model_name = options['model'].split('.')
        except ValueError:
            raise CommandError('expected app_label.modelname got \'{}\''.format(options['model']))
        model = django_apps.get_model(app_label, model_name)
        field_list = [field.name for field in model._meta.fields]
        self.stdout.write(
            self.style.NOTICE('Model \'{}\''.format(model._meta.verbose_name)))
        self.stdout.write(
            self.style.NOTICE('CSV \'{}\''.format(csv_filename.split('/')[-1:][0])))
        added = 0
        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            csv_row_count = len(data)
        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            header = None
            for recs, row in enumerate(reader):
                if not header:
                    header = row
                    entries_to_remove = [f for f in header if f not in field_list]
                else:
                    subject_identifier = row.get('subject_identifier')
                    try:
                        potential_subject = PotentialSubject.objects.get(
                            subject_identifier=subject_identifier)
                        for k in entries_to_remove:
                            row.pop(k, None)
                        model.objects.create(potential_subject=potential_subject, **row)
                        added += 1
                        self.stdout.write(
                            self.style.NOTICE(
                                '  adding record {} / {} / {}{}'.format(added, recs, csv_row_count, ' ' * 35)), ending='\r')
                    except IntegrityError:
                        pass  # model.objects.get(subject_identifier=row.get('subject_identifier'))
                    except PotentialSubject.DoesNotExist:
                        self.stdout.write(
                            self.style.NOTICE(
                                '  adding record {} / {} / {}  skipping {}'.format(
                                    added, recs, csv_row_count, subject_identifier)), ending='\r')
                        pass  # only import of this is a PotentialSubject
        self.stdout.write(
            self.style.SUCCESS('Successfully imported {} / {} records.{}'.format(added, recs, ' ' * 35)))
