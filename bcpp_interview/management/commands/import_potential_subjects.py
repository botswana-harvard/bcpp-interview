import os
import csv

from django.core.management.base import BaseCommand, CommandError

from bcpp_interview.models import PotentialSubject


class Command(BaseCommand):
    help = 'Import potential subjects'

    def add_arguments(self, parser):
        parser.add_argument('csv_filename', type=str)

    def handle(self, *args, **options):
        csv_filename = options['csv_filename']
        if not os.path.exists(csv_filename):
            raise CommandError('CSV file does not exist. Got {}'.format(csv_filename))
        with open(csv_filename, 'r', newline='') as f:
            reader = csv.reader(f)
            header = None
            for recs, row in enumerate(reader):
                if not header:
                    header = row  # ['subject_identifier', 'category', 'community', 'region']
                else:
                    PotentialSubject.objects.create(**dict(zip(header, row)))
        self.stdout.write(self.style.SUCCESS('Successfully imported "{}" PotentialSubject records'.format(recs)))
