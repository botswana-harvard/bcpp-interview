from django.apps import AppConfig as DjangoAppConfig

from edc_call_manager.apps import AppConfig as EdcCallManagerAppConfigParent


class AppConfig(DjangoAppConfig):
    name = 'call_manager'


class EdcCallManagerAppConfig(EdcCallManagerAppConfigParent):
    app_label = 'call_manager'
