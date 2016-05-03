from django.db import models
from simple_history.models import HistoricalRecords as AuditTrail
from edc_consent.models.fields.bw import IdentityFieldsMixin
from edc_consent.models.fields import (ReviewFieldsMixin, PersonalFieldsMixin, VulnerabilityFieldsMixin,
                                       CitizenFieldsMixin)
from edc_consent.models import BaseConsent
# from edc_sync.models import SyncModelMixin
from edc_registration.models.registered_subject import RegisteredSubject
from edc_consent.models import ObjectConsentManager
from edc_base.model.models.base_uuid_model import BaseUuidModel


class SubjectConsent(BaseConsent, IdentityFieldsMixin, ReviewFieldsMixin, PersonalFieldsMixin,
                     CitizenFieldsMixin, VulnerabilityFieldsMixin, BaseUuidModel):

    MIN_AGE_OF_CONSENT = 16
    MAX_AGE_OF_CONSENT = 64
    AGE_IS_ADULT = 18
    GENDER_OF_CONSENT = ['M', 'F']
    SUBJECT_TYPES = ['subject']

    # registered_subject = models.ForeignKey(RegisteredSubject)

    history = AuditTrail()

    objects = ObjectConsentManager()

    class Meta:
        app_label = 'bcpp_interview'
        get_latest_by = 'consent_datetime'
        unique_together = (('first_name', 'dob', 'initials', 'version'), )
        ordering = ('-created', )
