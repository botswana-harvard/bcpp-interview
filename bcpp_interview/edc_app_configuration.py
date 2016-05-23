from datetime import datetime

from django.conf import settings

from edc_configuration.convert import localize
from edc_consent.models import ConsentType
from edc_content_type_map.models.content_type_map_helper import ContentTypeMapHelper

study_start_datetime = datetime(2016, 5, 1, 0, 0, 0)
study_end_datetime = datetime(2017, 5, 1, 0, 0, 0)


class EdcAppConfiguration(object):

    def __init__(self, ):
        pass

    def prepare(self):
        """Updates content type maps then runs each configuration method
        with the corresponding class attribute.

        Configuration methods update default data in supporting tables."""
        print('Preparing edc configuration')
        print('* content type maps')
        ContentTypeMapHelper().populate()
        ContentTypeMapHelper().sync()
        self.update_or_create_consent_type()

    consent_type_setup = [
        {'app_label': 'bcpp_interview',
         'model_name': 'subjectconsent',
         'start_datetime': study_start_datetime,
         'end_datetime': study_end_datetime,
         'version': '1'}]

    def update_or_create_consent_type(self):
        print('* consent types')
        for item in self.consent_type_setup:
            if settings.USE_TZ:
                item['start_datetime'] = localize(item.get('start_datetime'))
                item['end_datetime'] = localize(item.get('end_datetime'))
            try:
                consent_type = ConsentType.objects.get(
                    version=item.get('version'),
                    app_label=item.get('app_label'),
                    model_name=item.get('model_name'))
                consent_type.start_datetime = item.get('start_datetime')
                consent_type.end_datetime = item.get('end_datetime')
                consent_type.save()
            except ConsentType.DoesNotExist:
                ConsentType.objects.create(**item)
