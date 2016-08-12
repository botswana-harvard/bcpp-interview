import sys

from django.db import connection
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import DataError


class Command(BaseCommand):

    help = 'Convert history_id from INT to UUID (run once)'

    def handle(self, *args, **options):
        cursor = connection.cursor()
        cursor.execute('show tables')
        rows = cursor.fetchall()
        errors = []
        for table in rows:
            if 'historical' in table[0]:
                sql = 'update ' + table[0] + ' set history_id=replace(UUID(), \'-\', \'\')'
                try:
                    cursor.execute(sql)
                    sys.stdout.write(' [X]' + table[0] + '\n')
                except DataError as e:
                    errors.append(str(e))
                    sys.stdout.write(' [ ]' + table[0] + ' (failed)\n')
        if errors:
            raise CommandError(errors)
