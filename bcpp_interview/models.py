from django.db import models
from django.conf import settings
from django.utils import timezone
from simple_history.models import HistoricalRecords as AuditTrail
from django_crypto_fields.fields.encrypted_text_field import EncryptedTextField

from edc_constants.choices import YES_NO
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_consent.models import BaseConsent, ConsentManager, ObjectConsentManager
from edc_consent.models.fields import (
    ReviewFieldsMixin, PersonalFieldsMixin, VulnerabilityFieldsMixin, CitizenFieldsMixin)
from edc_consent.models.fields.bw import IdentityFieldsMixin
from edc_registration.models.registered_subject import RegisteredSubject
from edc_sync.models import SyncModelMixin

from .identifier import GroupIdentifier, InterviewIdentifier
from .managers import (
    SubjectGroupItemManager, InterviewManager, SubjectGroupManager, RecordingManager,
    SubjectLossManager)

REGIONS = (
    ('central', 'Central'),
    ('north', 'North'),
    ('south', 'South')
)

CATEGORIES = (
    ('not_linked', 'Not linked-to-care'),
    ('linked_only', 'Linked-to-care only'),
    ('initiated', 'Initiated ART'),
)


LOSS_CATEGORIES = (
    ('afraid_to_reveal_status', 'Afraid others will learn my status'),
    ('spouse_refused', 'Spouse refused'),
    ('no_contact', 'Subject could not be contacted'),
    ('not_interested', 'Subject is not interested'),
    ('too_busy', 'Too busy, do not have time to participate'),
    ('OTHER', 'Other reason, please specify ...')
)


def timestamp():
    return timezone.now().strftime('%Y%m%d%H%M%S')


def group_identifier():
    return GroupIdentifier().identifier


def interview_identifier():
    return InterviewIdentifier().identifier


class SubjectConsent(SyncModelMixin, BaseConsent, IdentityFieldsMixin, ReviewFieldsMixin,
                     PersonalFieldsMixin, CitizenFieldsMixin, VulnerabilityFieldsMixin, BaseUuidModel):

    MIN_AGE_OF_CONSENT = 18
    MAX_AGE_OF_CONSENT = 64
    AGE_IS_ADULT = 18
    GENDER_OF_CONSENT = ['M', 'F']
    SUBJECT_TYPES = ['subject']

    registered_subject = models.ForeignKey(RegisteredSubject)

    history = AuditTrail()

    consent = ConsentManager()

    objects = ObjectConsentManager()

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name, self.identity, self.subject_identifier)

    class Meta:
        app_label = 'bcpp_interview'
        get_latest_by = 'consent_datetime'
        unique_together = (('first_name', 'dob', 'initials', 'version'), )
        ordering = ('created', )


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

    history = AuditTrail()

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

    history = AuditTrail()

    objects = SubjectGroupItemManager()

    def natural_key(self):
        return (self.subject_group, self.subject_consent)

    class Meta:
        app_label = 'bcpp_interview'
        get_latest_by = 'created'
        unique_together = (('subject_group', 'subject_consent'), )


class BaseInterview(SyncModelMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(
        null=True,
        editable=False)

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

    history = AuditTrail()

    objects = InterviewManager()

    def save(self, *args, **kwargs):
        self.report_datetime = self.interview_datetime
        super(BaseRecording, self).save(*args, **kwargs)

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

    report_datetime = models.DateTimeField(
        null=True,
        editable=False)

    label = models.CharField(
        max_length=25,
        null=True,
        help_text=(
            'Friendly name for this recording or partial recording '
            'e.g. part 1, part2, or may be left blank.'))

    start_datetime = models.DateTimeField(null=True)

    stop_datetime = models.DateTimeField(null=True)

    recording_time = models.CharField(
        max_length=10,
        null=True)

    sound_file = models.FileField(
        upload_to=str(settings.UPLOAD_FOLDER),
        null=True)

    sound_filename = models.CharField(
        max_length=150,
        unique=True)

    sound_filesize = models.FloatField(
        null=True,
        blank=True)

    comment = EncryptedTextField(
        verbose_name="Additional comment that may assist in analysis of this discussion",
        max_length=250,
        blank=True,
        null=True
    )

    history = AuditTrail()

    objects = RecordingManager()

    def save(self, *args, **kwargs):
        if not self.label:
            self.label = self.sound_filename.split('/')[-1:][0]
        self.report_datetime = self.start_datetime
        super(BaseRecording, self).save(*args, **kwargs)

    def natural_key(self):
        return self.sound_filename

    class Meta:
        abstract = True


class InterviewRecording(BaseRecording):

    interview = models.ForeignKey(Interview)

    verified = models.CharField(
        max_length=10,
        choices=YES_NO,
        help_text='Indicate if the subject has agreed that this recording may be used for analysis')

    class Meta:
        app_label = 'bcpp_interview'
        get_latest_by = 'start_datetime'


class GroupDiscussionRecording(BaseRecording):

    group_discussion = models.ForeignKey(GroupDiscussion)

    verified = models.CharField(
        max_length=10,
        choices=YES_NO,
        help_text='Indicate if the group members have agreed that this recording may be used for analysis')

    class Meta:
        app_label = 'bcpp_interview'
        get_latest_by = 'start_datetime'


class PotentialSubject(BaseUuidModel):

    registered_subject = models.ForeignKey(RegisteredSubject, null=True)

    subject_identifier = models.CharField(
        max_length=25,
        editable=False,
        unique=True)

    category = models.CharField(
        max_length=25,
        choices=CATEGORIES)

    community = models.CharField(
        max_length=25)

    region = models.CharField(
        max_length=25,
        choices=REGIONS)

    history = AuditTrail()

    def __str__(self):
        return self.subject_identifier

    class Meta:
        app_label = 'bcpp_interview'


class SubjectLoss(SyncModelMixin, BaseUuidModel):

    potential_subject = models.ForeignKey(PotentialSubject)

    registered_subject = models.ForeignKey(RegisteredSubject, editable=False)

    subject_identifier = models.CharField(
        max_length=25,
        unique=True,
        editable=False)

    report_datetime = models.DateTimeField(
        default=timezone.now)

    reason = models.CharField(
        max_length=25,
        choices=LOSS_CATEGORIES)

    reason_other = EncryptedTextField(
        verbose_name="Other reason",
        max_length=250,
        blank=True,
        null=True
    )

    history = AuditTrail()

    objects = SubjectLossManager()

    def __str__(self):
        return self.subject_identifier

    def save(self, *args, **kwargs):
        self.subject_identifier = self.potential_subject.subject_identifier
        self.registered_subject = self.potential_subject.registered_subject
        super(BaseRecording, self).save(*args, **kwargs)

    def natural_key(self):
        return self.subject_identifier

    class Meta:
        app_label = 'bcpp_interview'
