from datetime import datetime

from django.apps import AppConfig

from edc_consent.apps import EdcConsentAppConfig
from edc_map.apps import EdcMapAppConfig


class BcppInterviewAppConfig(AppConfig):
    name = 'bcpp_interview'
    verbose_name = 'BCPP Interview'


class BcppInterviewMapAppConfig(EdcMapAppConfig):
    name = 'bcpp_map'
    verbose_name = 'BCPP Interview Mappers'
    mapper_model = ('bcpp_interview', 'subjectlocation')
    mapper_survey_model = ('bcpp_interview', 'survey')
    verify_point_on_save = False


class ConsentAppConfig(EdcConsentAppConfig):
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
