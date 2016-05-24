from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        User.objects.create(is_superuser=True, username='django',
                            password=make_password('cc3721b'), is_staff=True, is_active=True)
