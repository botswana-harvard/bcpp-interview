import csv
import os

from dateutil import parser
from django.apps import apps as django_apps
from django.core.management.base import BaseCommand, CommandError
from bcpp_interview.models import PotentialSubject, SubjectLocation
from edc_map.exceptions import MapperError
from django.db.utils import IntegrityError


class Command(BaseCommand):

    """Import model data from CSV.

    For example:
        python manage.py load_production_data bcpp_interview.rawdata /Users/erikvw/Documents/bcpp/qualitative_substudy_subject_list10may2016_with_plots.csv
    """

    help = 'Load CSV data into a model'

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
        self.stdout.write(
            self.style.SUCCESS('Model \'{}\''.format(model._meta.verbose_name)))
        self.stdout.write(
            self.style.SUCCESS('CSV \'{}\''.format(csv_filename.split('/')[-1:][0])))
        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            header = None
            for recs, row in enumerate(reader):
                if not header:
                    header = row
                else:
                    try:
                        obj = model.objects.create(**row)
                    except IntegrityError:
                        obj = model.objects.get(subject_identifier=row.get('subject_identifier'))
                    self.create_handler(obj, row)
                print('  adding record {}'.format(recs), end='\r')
        self.stdout.write(
            self.style.SUCCESS('Successfully imported {} records'.format(recs)))

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
        sub_category = None
        if category == 'Initiated ART':
            if eligibility_category == 'CD4<=350':
                sub_category = 'national_guidelines'
            elif 'VL>10000' in eligibility_category:
                sub_category = 'expanded_guidelines'
        return sub_category
