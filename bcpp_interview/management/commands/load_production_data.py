import csv
import os

from dateutil import parser
from django.apps import apps as django_apps
from django.core.management.base import BaseCommand, CommandError
from bcpp_interview.models import PotentialSubject, SubjectLocation
from edc_map.exceptions import MapperError
from django.db.utils import IntegrityError
from edc_constants.constants import NOT_APPLICABLE


class Command(BaseCommand):

    """Import model data from CSV.

    For example:
        python manage.py load_production_data bcpp_interview.rawdata /Users/erikvw/Documents/bcpp/qualitative_substudy/qualitative_substudy_subject_list10may2016_with_plots.csv

        python manage.py load_production_data bcpp_interview.rawdata /home/django/qualitative_substudy_subject_list10may2016_with_plots.csv
    """

    help = 'Load CSV data into a model'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help='A model\'s app_label.model_name')
        parser.add_argument('csv_filename', type=str, help='Full path to CSV file')

    def handle(self, *args, **options):
        csv_filename = options['csv_filename']
        if not os.path.exists(csv_filename):
            raise CommandError('Csv file does not exist. Got {}'.format(csv_filename))
        try:
            app_label, model_name = options['model'].split('.')
        except ValueError:
            raise CommandError('Expected app_label.modelname got \'{}\''.format(options['model']))
        model = django_apps.get_model(app_label, model_name)
        self.stdout.write(
            self.style.NOTICE('Data source: csv \'{}\''.format(csv_filename.split('/')[-1:][0])))
        self.stdout.write(
            self.style.NOTICE('Target model: \'{}\''.format(model._meta.verbose_name)))
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
                else:
                    try:
                        obj = model.objects.create(**row)
                        added += 1
                        self.stdout.write(
                            self.style.NOTICE('  adding record {} / {} / {}{}'.format(added, recs, csv_row_count, ' ' * 35)), ending='\r')
                    except IntegrityError:
                        obj = model.objects.get(subject_identifier=row.get('subject_identifier'))
                        self.stdout.write(
                            self.style.NOTICE('  processing existing record {} / {} / {}{}'.format(added, recs, csv_row_count, ' ' * 35)), ending='\r')
                    self.create_handler(obj, row)
        self.stdout.write(
            self.style.SUCCESS('Successfully added {} / {} / {} records{}'.format(added, recs, csv_row_count, ' ' * 35)))

    def create_handler(self, obj, row):
        try:
            PotentialSubject.objects.create(
                subject_identifier=obj.subject_identifier,
                identity=obj.identity,
                dob=parser.parse(obj.dob),
                gender=obj.gender,
                category=obj.issue,
                sub_category=self.sub_category(obj.issue, obj.elig_cat),
                community=obj.community,
            )
        except IntegrityError as e:
            self.stdout.write(
                self.style.WARNING('IntegrityError: {}. Got {}.'.format(
                    obj.subject_identifier, str(e))))
        try:
            SubjectLocation.objects.create(
                subject_identifier=obj.subject_identifier,
                gps_confirm_latitude=obj.latitude,
                gps_confirm_longitude=obj.longitude,
                community=obj.community,
            )
        except MapperError as e:
            self.stdout.write(
                self.style.ERROR('MapperError: {}. Got {}'.format(
                    obj.subject_identifier, str(e))))
        except IntegrityError:
            pass

    def sub_category(self, category, eligibility_category):
        sub_category = NOT_APPLICABLE
        if category == 'Initiated ART':
            if eligibility_category == 'CD4<=350':
                sub_category = 'national_guidelines'
            elif 'VL>10000' in eligibility_category:
                sub_category = 'expanded_guidelines'
        return sub_category
