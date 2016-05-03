import factory
from django.utils import timezone
from datetime import timedelta
from bcpp_interview.models import SubjectConsent
from django.test.testcases import TestCase
from edc_consent.models import ConsentType
from edc_constants.constants import YES


class ConsentTypeFactory(factory.DjangoModelFactory):

    class Meta:
        model = ConsentType

    version = '1.0'
    updates_version = None
    app_label = 'edc_consent'
    model_name = 'subjectconsent'
    start_datetime = timezone.now() - timedelta(days=1)
    end_datetime = timezone.now() + timedelta(days=365)


class TestConsent(TestCase):

    def setUp(self):
        ConsentTypeFactory(app_label='bcpp_interview', model_name='subjectconsent')

    def test_consent(self):
        options = {
            'first_name': 'ERIK',
            'last_name': 'WIDE',
            'initials': 'EW',
            'identity': '123456789',
            'identity_type': 'OMANG',
            'confirm_identity': '123456789',
            'consent_datetime': timezone.now(),
            'is_literate': YES,
            'citizen': YES,
        }
        SubjectConsent.objects.create(**options)
        SubjectConsent.objects.get(first_name='ERIK')
