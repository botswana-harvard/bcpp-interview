from django.core.management.base import BaseCommand, CommandError
from bcpp_interview.models import (
    PotentialSubject, LINKED_ONLY, NOT_LINKED,
    INITIATED, INITIATED_T1, DEFAULTER)

"""
referred never linked  (IDI and/or FGD if possible)
referred, linked and did not start (IDI)
referred, linked, initiated (expanded criteria) (IDI and FGD)
referred, linked, initiated (national criteria) (IDI and FGD)
referred, linked and initiated after T1 (IDI)
defaulters (IDI)
"""

category_map = {
    'Initiated after T1 Visit': INITIATED_T1,
    'DEFAULTER': DEFAULTER,
    'Did Not Link': NOT_LINKED,
    'Initiated ART': INITIATED,
    'Link, Not Initiated': LINKED_ONLY,
    INITIATED: INITIATED,
    LINKED_ONLY: LINKED_ONLY,
    NOT_LINKED: NOT_LINKED}


class Command(BaseCommand):

    help = 'Update categories in Potential Subject'

    def handle(self, *args, **options):

        for obj in PotentialSubject.objects.all():
            try:
                obj.category = category_map[obj.category]
                obj.save()
            except KeyError:
                raise CommandError('Unknown category. Got {}'.format(obj.category))
        recs = PotentialSubject.objects.all().count()
        self.stdout.write(
            self.style.SUCCESS('Successfully updated the category for {} records'.format(recs)))
