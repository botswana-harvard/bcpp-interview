from django.db import models
from django.conf import settings
from django.utils import timezone
from simple_history.models import HistoricalRecords as AuditTrail

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_consent.models import BaseConsent, ConsentManager, ObjectConsentManager
from edc_consent.models.fields import (
    ReviewFieldsMixin, PersonalFieldsMixin, VulnerabilityFieldsMixin, CitizenFieldsMixin)
from edc_consent.models.fields.bw import IdentityFieldsMixin
from edc_registration.models.registered_subject import RegisteredSubject
from edc_sync.models import SyncModelMixin

from .identifier import GroupIdentifier, InterviewIdentifier
from .managers import SubjectGroupItemManager, InterviewManager, SubjectGroupManager, RecordingManager

CATEGORIES = (
    ('not_linked', 'Not linked-to-care'),
    ('linked_only', 'Linked-to-care only'),
    ('initiated', 'Initiated ART'),
)


def timestamp():
    return timezone.now().strftime('%Y%m%d%H%M%S')


def group_identifier():
    return GroupIdentifier().identifier


def interview_identifier():
    return InterviewIdentifier().identifier


class SubjectConsent(SyncModelMixin, BaseConsent, IdentityFieldsMixin, ReviewFieldsMixin,
                     PersonalFieldsMixin, CitizenFieldsMixin, VulnerabilityFieldsMixin, BaseUuidModel):

    MIN_AGE_OF_CONSENT = 16
    MAX_AGE_OF_CONSENT = 64
    AGE_IS_ADULT = 18
    GENDER_OF_CONSENT = ['M', 'F']
    SUBJECT_TYPES = ['subject']

    registered_subject = models.ForeignKey(RegisteredSubject, null=True)

    history = AuditTrail()

    consent = ConsentManager()

    objects = ObjectConsentManager()

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name, self.identity, self.subject_identifier)

    class Meta:
        app_label = 'bcpp_interview'
        get_latest_by = 'consent_datetime'
        unique_together = (('first_name', 'dob', 'initials', 'version'), )
        ordering = ('-created', )


class SubjectGroup(SyncModelMixin, BaseUuidModel):

    group_name = models.CharField(
        max_length=5,
        default=group_identifier,
        unique=True)

    size = models.IntegerField(
        verbose_name="How many consented subjects are in this group?")

    category = models.CharField(
        verbose_name='Members of this group have ...',
        max_length=25,
        choices=CATEGORIES)

    community = models.CharField(max_length=25)

    objects = SubjectGroupManager()

    def __str__(self):
        return 'Group \'{}\' by {} on {}'.format(self.group_name, self.user_created, self.created.strftime('%Y-%m-%d'))

    def natural_key(self):
        return self.group_name

    class Meta:
        app_label = 'bcpp_interview'
        get_latest_by = 'created'


class SubjectGroupItem(SyncModelMixin, BaseUuidModel):

    subject_group = models.ForeignKey(SubjectGroup)

    subject_consent = models.ForeignKey(SubjectConsent)

    category = models.CharField(
        max_length=25,
        choices=CATEGORIES)

    objects = SubjectGroupItemManager()

    def natural_key(self):
        return (self.subject_group, self.subject_consent)

    class Meta:
        app_label = 'bcpp_interview'
        get_latest_by = 'created'
        unique_together = (('subject_group', 'subject_consent'), )


class BaseInterview(SyncModelMixin, BaseUuidModel):

    interview_name = models.CharField(
        max_length=7,
        default=interview_identifier,
        unique=True)

    interview_datetime = models.DateTimeField(default=timezone.now)

    category = models.CharField(
        max_length=25,
        choices=CATEGORIES)

    community = models.CharField(
        verbose_name='Community',
        max_length=25,
    )

    location = models.TextField(
        verbose_name='Where is this interview being conducted?',
        max_length=100,
    )

    interviewed = models.BooleanField(default=False, editable=False)

    objects = InterviewManager()

    def natural_key(self):
        return self.interview_name

    class Meta:
        abstract = True


class Interview(BaseInterview):

    subject_consent = models.ForeignKey(SubjectConsent)

    def __str__(self):
        return self.subject_consent.subject_identifier

    class Meta:
        app_label = 'bcpp_interview'
        get_latest_by = 'interview_datetime'


class GroupDiscussion(BaseInterview):

    subject_group = models.ForeignKey(SubjectGroup)

    def __str__(self):
        return self.subject_group.group_name

    class Meta:
        app_label = 'bcpp_interview'
        get_latest_by = 'interview_datetime'


class BaseRecording(SyncModelMixin, BaseUuidModel):

    start_datetime = models.DateTimeField(null=True, editable=False)

    stop_datetime = models.DateTimeField(null=True, editable=False)

    recording_time = models.FloatField(null=True, editable=False)

    sound_file = models.FileField(
        upload_to=str(settings.UPLOAD_FOLDER),
        null=True)

    sound_filename = models.CharField(
        max_length=150,
        unique=True)

    sound_filesize = models.FloatField(
        null=True,
        blank=True)

    objects = RecordingManager()

    def natural_key(self):
        return self.sound_filename

    class Meta:
        abstract = True


class InterviewRecording(BaseRecording):

    interview = models.ForeignKey(Interview)

    class Meta:
        app_label = 'bcpp_interview'
        get_latest_by = 'start_datetime'


class GroupDiscussionRecording(BaseRecording):

    group_discussion = models.ForeignKey(GroupDiscussion)

    class Meta:
        app_label = 'bcpp_interview'
        get_latest_by = 'start_datetime'
