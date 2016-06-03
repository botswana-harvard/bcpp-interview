from django.apps import AppConfig
from django.db.models.signals import post_migrate

from edc_map.apps import EdcMapAppConfig


class BcppInterviewAppConfig(AppConfig):
    name = 'bcpp_interview'
    verbose_name = 'BCPP Interview'

    def ready(self):
        def edc_configure_callback(sender, **kwargs):
            from .edc_app_configuration import EdcAppConfiguration
            edc_app_configuration = EdcAppConfiguration()
            edc_app_configuration.prepare()
        post_migrate.connect(edc_configure_callback, sender=self)


class BcppInterviewMapAppConfig(EdcMapAppConfig):
    name = 'bcpp_map'
    verbose_name = 'BCPP Interview Mappers'
    mapper_model = ('bcpp_interview', 'subjectlocation')
    mapper_survey_model = ('bcpp_interview', 'survey')
    verify_point_on_save = False
