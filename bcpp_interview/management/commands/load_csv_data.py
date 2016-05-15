import csv
import os

from django.db.utils import IntegrityError
from django.apps import apps as django_apps
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
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
        if model_name == 'potentialsubject':
            columns = ['community', 'subject_identifier', 'category', 'identity']
        with open(csv_filename, 'r', newline='') as f:
            reader = csv.reader(f)
            header = None
            for recs, row in enumerate(reader):
                if not header:
                    header = True
                else:
                    try:
                        model.objects.create(**dict(zip(columns, [row[1], row[2], row[3], row[5]])))
                    except TypeError as e:
                        raise CommandError(str(e))
                    except IntegrityError as e:
                        print(str(e), [row[1], row[2], row[3]])
        self.stdout.write(
            self.style.SUCCESS('Successfully imported {} records'.format(recs)))
