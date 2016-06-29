from datetime import datetime

from django.apps import AppConfig
from django.conf import settings
from django_crypto_fields.apps import DjangoCryptoFieldsAppConfig as DjangoCryptoFieldsAppConfigParent

from edc_consent.apps import EdcConsentAppConfig as EdcConsentAppConfigParent
from edc_map.apps import EdcMapAppConfig as EdcMapAppConfigParent
from edc_sync.apps import EdcSyncAppConfig as EdcSyncAppConfigParent
from edc_sync.constants import SERVER

try:
    edc_sync_role = settings.EDC_SYNC_ROLE
except AttributeError:
    edc_sync_role = SERVER


class BcppInterviewAppConfig(AppConfig):
    name = 'bcpp_interview'
    institution = 'Botswana Harvard AIDS Institute Partnership'
    verbose_name = 'BCPP Interview'


class BcppMapAppConfig(EdcMapAppConfigParent):
    name = 'bcpp_map'
    verbose_name = 'BCPP Interview Mappers'
    mapper_model = ('bcpp_interview', 'subjectlocation')
    mapper_survey_model = ('bcpp_interview', 'survey')
    verify_point_on_save = False
    zoom_levels = ['14', '15', '16', '17', '18']


class EdcConsentAppConfig(EdcConsentAppConfigParent):
    consent_type_setup = [
        {'app_label': 'bcpp_interview',
         'model_name': 'subjectconsent',
         'start_datetime': datetime(2016, 5, 1, 0, 0, 0),
         'end_datetime': datetime(2017, 5, 1, 0, 0, 0),
         'version': '1'},
        {'app_label': 'bcpp_interview',
         'model_name': 'nurseconsent',
         'start_datetime': datetime(2016, 5, 1, 0, 0, 0),
         'end_datetime': datetime(2017, 5, 1, 0, 0, 0),
         'version': '1'}]


class DjangoCryptoFieldsAppConfig(DjangoCryptoFieldsAppConfigParent):
    name = 'django_crypto_fields'
    model = ('django_crypto_fields', 'crypt')


class EdcSyncAppConfig(EdcSyncAppConfigParent):
    name = 'edc_sync'
    role = edc_sync_role
