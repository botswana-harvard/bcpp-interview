import os
from datetime import datetime

from django.apps import AppConfig
from django.conf import settings

from edc_base.apps import AppConfig as EdcBaseAppConfigParent
from edc_consent.apps import EdcConsentAppConfig as EdcConsentAppConfigParent
from edc_map.apps import AppConfig as EdcMapAppConfigParent
from edc_sync.apps import AppConfig as EdcSyncAppConfigParent
from edc_sync.constants import SERVER, CLIENT
from edc_sync_files.apps import AppConfig as EdcSyncFileAppConfigParent


class EdcBaseAppConfig(EdcBaseAppConfigParent):
    institution = 'Botswana Harvard AIDS Institute Partnership'
    project_name = 'BCPP Interview'


class BcppInterviewAppConfig(AppConfig):
    name = 'bcpp_interview'
    verbose_name = 'BCPP Interview'


class EdcMapAppConfig(EdcMapAppConfigParent):
    verbose_name = 'BCPP Interview Mappers'
    mapper_model = ('bcpp_interview', 'subjectlocation')
    mapper_survey_model = ('bcpp_interview', 'survey')
    landmark_model = ('bcpp_map', 'landmark')
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


class EdcSyncAppConfig(EdcSyncAppConfigParent):
    role = SERVER


class EdcSyncFileAppConfig(EdcSyncFileAppConfigParent):

    # these attrs will be overwritten with values in edc_sync.ini, see ready()
    config_attrs = {
        'edc_sync_files': ['user', 'role', 'device_ip', 'source_folder', 'destination_folder'],
        'corsheaders': [('cors_origin_whitelist', tuple), ('cors_origin_allow_all', bool)]
    }
    edc_sync_upload = os.path.join(settings.BASE_DIR, "media", "upload")
    media_folders = [edc_sync_upload]
    role = SERVER
