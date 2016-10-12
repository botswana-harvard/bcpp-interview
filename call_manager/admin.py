from django.contrib import admin
from django.contrib.admin.options import StackedInline

from simple_history.admin import SimpleHistoryAdmin

from edc_base.modeladmin.mixins import (
    ModelAdminAuditFieldsMixin,
    ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin, ModelAdminModelRedirectMixin)
from edc_call_manager.admin import (
    ModelAdminCallMixin, ModelAdminLogMixin, ModelAdminLogEntryMixin,
    ModelAdminLogEntryInlineMixin, edc_call_manager_admin)

from .models import Call, Log, LogEntry


class BaseModelAdmin(ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin):
    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'


class ModelAdminStackedInlineMixin(ModelAdminAuditFieldsMixin, StackedInline):
    pass


@admin.register(Call, site=edc_call_manager_admin)
class CallAdmin(BaseModelAdmin, ModelAdminCallMixin, SimpleHistoryAdmin):

    subject_app = 'bcpp_interview'
    subject_model = 'potentialsubject'

    list_display_pos = ((1, 'map_button'), (7, 'log_entry_appt_date'),)

    list_filter = ('potential_subject__category', 'potential_subject__sub_category', 'potential_subject__community')

    def log_entry_appt_date(self, obj):
        log_entry = LogEntry.objects.filter(log__call=obj).order_by('-created').first()
        if log_entry:
            return '{}'.format(log_entry.appt_date)
        else:
            return ''
    log_entry_appt_date.short_description = 'APPT_DATE'

    def map_button(self, obj):
        return self.button(
            'location_url',
            (obj.potential_subject.map_area, obj.potential_subject.subject_identifier, ),
            label='map')
    map_button.short_description = 'map'


class LogEntryInlineAdmin(ModelAdminLogEntryInlineMixin, ModelAdminStackedInlineMixin):

    model = LogEntry


@admin.register(Log, site=edc_call_manager_admin)
class LogAdmin(BaseModelAdmin, ModelAdminModelRedirectMixin, ModelAdminLogMixin, SimpleHistoryAdmin):

    list_filter = ('call__potential_subject__category', 'call__potential_subject__sub_category',
                   'call__potential_subject__community')


@admin.register(LogEntry, site=edc_call_manager_admin)
class LogEntryAdmin(BaseModelAdmin, ModelAdminLogEntryMixin, SimpleHistoryAdmin):

    list_filter = ('log__call__potential_subject__category', 'log__call__potential_subject__sub_category',
                   'log__call__potential_subject__community')
