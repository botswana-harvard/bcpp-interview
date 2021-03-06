from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            User.objects.create(is_superuser=True, username='django',
                                password=make_password('django'), is_staff=True, is_active=True)
        except IntegrityError:
            raise CommandError('User already exists')
