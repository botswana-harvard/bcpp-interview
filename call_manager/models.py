from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from simple_history.models import HistoricalRecords as AuditTrail

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_call_manager.constants import NO_CONTACT
from edc_call_manager.managers import CallManager, LogManager, LogEntryManager
from edc_call_manager.models import CallModelMixin, LogModelMixin, LogEntryModelMixin
from edc_sync.models.sync_model_mixin import SyncModelMixin

from bcpp_interview.models import PotentialSubject


class Call(SyncModelMixin, CallModelMixin, BaseUuidModel):

    potential_subject = models.ForeignKey(PotentialSubject)

    history = AuditTrail()

    objects = CallManager()

    def __str__(self):
        return self.subject_identifier

    @property
    def subject(self):
        return self.potential_subject

    class Meta:
        app_label = 'call_manager'


class Log(SyncModelMixin, LogModelMixin, BaseUuidModel):

    call = models.ForeignKey(Call)

    history = AuditTrail()

    objects = LogManager()

    class Meta:
        app_label = 'call_manager'


class LogEntry(SyncModelMixin, LogEntryModelMixin, BaseUuidModel):

    log = models.ForeignKey(Log)

    history = AuditTrail()

    objects = LogEntryManager()

    class Meta:
        app_label = 'call_manager'


@receiver(post_save, sender=LogEntry, dispatch_uid='post_save_bcpp_interview_call')
def post_save_bcpp_interview_call(sender, instance, raw, created, using, update_fields, **kwargs):
    if not raw:
        if instance.contact_type != NO_CONTACT:
            instance.log.call.potential_subject.contacted = True
            instance.log.call.potential_subject.save(update_fields=['contacted', 'modified'])
