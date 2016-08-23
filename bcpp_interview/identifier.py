from edc_identifier.short_identifier import ShortIdentifier

from django.apps import apps as django_apps

app_config_device = django_apps.get_app_config('edc_device')


class GroupIdentifier(ShortIdentifier):

    identifier_pattern = r'^[A-Z0-9]{5}$'
    prefix_pattern = '[0-9]{2}'
    random_string_pattern = r'^[A-Z0-9]{5}$'

    def __init__(self):
        prefix = app_config_device.device_id
        super(GroupIdentifier, self).__init__(options={'prefix': prefix})


class InterviewIdentifier(ShortIdentifier):

    identifier_pattern = r'^[A-Z0-9]{5}$'
    prefix_pattern = '[0-9]{2}'
    random_string_pattern = r'^[A-Z0-9]{5}$'

    def __init__(self):
        prefix = app_config_device.device_id
        super(InterviewIdentifier, self).__init__(options={'prefix': prefix})
