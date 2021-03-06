from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django_crypto_fields.fields import (
    EncryptedTextField, IdentityField, FirstnameField, LastnameField, EncryptedCharField)

from edc_audio_recording.models import RecordingModelMixin, RecordingManager
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_call_manager.mixins import CallLogLocatorMixin
from edc_consent.model_mixins import ConsentModelMixin, ConsentManager
from edc_consent.field_mixins import (
    ReviewFieldsMixin, PersonalFieldsMixin, VulnerabilityFieldsMixin, CitizenFieldsMixin)
from edc_consent.field_mixins.bw import IdentityFieldsMixin
from edc_constants.choices import YES_NO, GENDER
from edc_constants.constants import NO, NOT_APPLICABLE, MALE, FEMALE
from edc_identifier.subject.classes import SubjectIdentifier
from edc_locator.models import LocatorMixin
from edc_map.model_mixins import MapperModelMixin
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords

from .identifier import GroupIdentifier, InterviewIdentifier
from .managers import (
    FocusGroupItemManager, InterviewManager, FocusGroupManager,
    SubjectLossManager, GroupDiscussionLabelManager, PotentialSubjectManager,
    SubjectConsentManager, NurseConsentManager, SubjectLocatorManager, SubjectLocationManager)


NOT_LINKED = 'not_linked'
LINKED_ONLY = 'linked_only'
INITIATED = 'initiated'
INITIATED_T1 = 't1_initiated'
DEFAULTER = 'DEFAULTER'

INITIATED_NATIONAL_GUIDELINES = 'national_guidelines'
INITIATED_EXPANDED_GUIDELINES = 'expanded_guidelines'


REGIONS = (
    ('central', 'Central'),
    ('north', 'North'),
    ('south', 'South')
)

CATEGORIES = (
    (NOT_LINKED, 'Not linked-to-care'),
    (LINKED_ONLY, 'Linked-to-care only'),
    (DEFAULTER, 'Defaulter'),
    (INITIATED, 'Initiated ART'),
    (INITIATED_T1, 'Initiated ART at T1'),
)

SUB_CATEGORIES = (
    (INITIATED_NATIONAL_GUIDELINES, 'by national guidelines'),
    (INITIATED_EXPANDED_GUIDELINES, 'by expanded guidelines'),
    (NOT_APPLICABLE, 'Not applicable'),
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


class NurseConsent(SyncModelMixin, ConsentModelMixin, IdentityFieldsMixin, ReviewFieldsMixin,
                   PersonalFieldsMixin, CitizenFieldsMixin, VulnerabilityFieldsMixin, BaseUuidModel):

    MIN_AGE_OF_CONSENT = 18
    MAX_AGE_OF_CONSENT = 99
    AGE_IS_ADULT = 18
    GENDER_OF_CONSENT = [MALE, FEMALE]
    SUBJECT_TYPES = ['nurse']

    interviewed = models.BooleanField(default=False, editable=False)

    idi = models.BooleanField(default=False, editable=False)

    fgd = models.BooleanField(default=False, editable=False)

    history = SyncHistoricalRecords()

    consent = ConsentManager()

    objects = NurseConsentManager()

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name, self.identity, self.subject_identifier)

    def natural_key(self):
        return (self.subject_identifier, )

    def save(self, *args, **kwargs):
        if not self.id:
            self.subject_identifier = SubjectIdentifier(site_code='99').get_identifier()
        super(NurseConsent, self).save(*args, **kwargs)

    class Meta(ConsentModelMixin.Meta):
        app_label = 'bcpp_interview'


class PotentialSubject(BaseUuidModel):

    identity = IdentityField(
        verbose_name="Identity",
        unique=True,
        help_text=("Use Omang, Passport number, driver's license number or Omang receipt number")
    )

    subject_identifier = models.CharField(
        max_length=25,
        unique=True)

    first_name = FirstnameField(
        verbose_name="First name",
        null=True,
    )

    last_name = LastnameField(
        verbose_name="Last name",
        null=True,
    )

    initials = EncryptedCharField(
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message=('Ensure initials consist of letters '
                     'only in upper case, no spaces.')), ],
        null=True,
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER,
        null=True)

    dob = models.DateField(null=True)

    contacted = models.BooleanField(default=False, editable=False)

    consented = models.BooleanField(default=False, editable=False)

    interviewed = models.BooleanField(default=False, editable=False)

    idi = models.BooleanField(default=False, editable=False)

    fgd = models.BooleanField(default=False, editable=False)

    category = models.CharField(
        max_length=25,
        choices=CATEGORIES)

    sub_category = models.CharField(
        max_length=25,
        default=NOT_APPLICABLE,
        choices=SUB_CATEGORIES,
        help_text='Note: only applicable if subjects are initiated')

    community = models.CharField(
        max_length=25)

    pair = models.IntegerField(
        null=True)

    region = models.CharField(
        max_length=25,
        choices=REGIONS)

    source = models.CharField(
        max_length=25,
        null=True,
        help_text='')

    history = SyncHistoricalRecords()

    objects = PotentialSubjectManager()

    def natural_key(self):
        return (self.subject_identifier, )

    @property
    def subject_consent(self):
        try:
            subject_consent = SubjectConsent.objects.get(subject_identifier=self.subject_identifier)
        except SubjectConsent.DoesNotExist:
            return None
        return subject_consent

    def __str__(self):
        try:
            subject_consent = SubjectConsent.objects.get(potential_subject=self)
            first_name = subject_consent.first_name
            last_name = subject_consent.last_name
            name = first_name + ' ' + last_name
        except SubjectConsent.DoesNotExist:
            name = 'not consented'
        return '{}. {}. {}'.format(
            name, self.get_category_display(), self.subject_identifier)

    @property
    def map_area(self):
        return self.community.replace(' ', '_').lower()

    class Meta:
        app_label = 'bcpp_interview'


class SubjectConsent(SyncModelMixin, ConsentModelMixin, IdentityFieldsMixin, ReviewFieldsMixin,
                     PersonalFieldsMixin, CitizenFieldsMixin, VulnerabilityFieldsMixin, BaseUuidModel):

    MIN_AGE_OF_CONSENT = 18
    MAX_AGE_OF_CONSENT = 64
    AGE_IS_ADULT = 18
    GENDER_OF_CONSENT = [MALE, FEMALE]
    SUBJECT_TYPES = ['subject']

    potential_subject = models.ForeignKey(PotentialSubject)

    history = SyncHistoricalRecords()

    consent = ConsentManager()

    objects = SubjectConsentManager()

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name, self.identity, self.subject_identifier)

    def natural_key(self):
        return (self.subject_identifier, )

    def save(self, *args, **kwargs):
        if not self.id:
            potential_subject = self.fetch_potential_subject(self.identity)
            self.subject_identifier = potential_subject.subject_identifier
            self.potential_subject = potential_subject
        super(SubjectConsent, self).save(*args, **kwargs)

    @classmethod
    def fetch_potential_subject(cls, identity=None, exception_class=None):
        exception_class = exception_class or ValidationError
        try:
            potential_subject = PotentialSubject.objects.get(identity=identity)
        except PotentialSubject.DoesNotExist:
            raise exception_class(
                'Potential subject with identity \'{}\' was not found.'.format(identity))
        return potential_subject

    class Meta(ConsentModelMixin.Meta):
        app_label = 'bcpp_interview'


class SubjectLocator(LocatorMixin, CallLogLocatorMixin, BaseUuidModel):

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        editable=False,
        null=True,
        unique=True)

    potential_subject = models.OneToOneField(PotentialSubject)

    history = SyncHistoricalRecords()

    objects = SubjectLocatorManager()

    def __str__(self):
        return self.potential_subject.subject_identifier

    def natural_key(self):
        return self.potential_subject.natural_key()
    natural_key.dependencies = ['bcpp_interview.potentialsubject']

    def get_call_log_options(self):
        return dict(call__potential_subject=self.potential_subject)

    class Meta:
        app_label = 'bcpp_interview'


class FocusGroup(SyncModelMixin, BaseUuidModel):

    reference = models.CharField(
        max_length=15,
        default=group_identifier,
        unique=True)

    size = models.IntegerField(
        verbose_name="How many consented subjects are in this focus group?")

    category = models.CharField(
        max_length=25,
        choices=CATEGORIES)

    sub_category = models.CharField(
        max_length=25,
        choices=SUB_CATEGORIES,
        help_text='Note: only applicable if subjects are initiated')

    history = SyncHistoricalRecords()

    objects = FocusGroupManager()

    def __str__(self):
        return self.reference

    def natural_key(self):
        return (self.reference, )

    class Meta:
        app_label = 'bcpp_interview'
        get_latest_by = 'created'


class FocusGroupItem(SyncModelMixin, BaseUuidModel):

    focus_group = models.ForeignKey(FocusGroup)

    potential_subject = models.ForeignKey(PotentialSubject)

    history = SyncHistoricalRecords()

    objects = FocusGroupItemManager()

    def __str__(self):
        return self.potential_subject.subject_identifier

    def natural_key(self):
        return self.focus_group.natural_key() + self.potential_subject.natural_key()
    natural_key.dependencies = ['bcpp_interview.focusgroup', 'bcpp_interview.potentialsubject']

    class Meta:
        app_label = 'bcpp_interview'
        get_latest_by = 'created'
        unique_together = (('focus_group', 'potential_subject'), )


class BaseInterview(SyncModelMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(
        null=True,
        editable=False)

    reference = models.CharField(
        max_length=7,
        default=interview_identifier,
        unique=True)

    interview_datetime = models.DateTimeField(default=timezone.now)

    location = models.TextField(
        verbose_name='Where is this interview being conducted?',
        max_length=100,
    )

    interviewed = models.BooleanField(default=False, editable=False)

    def save(self, *args, **kwargs):
        self.report_datetime = self.interview_datetime
        super(BaseInterview, self).save(*args, **kwargs)

    def natural_key(self):
        return (self.reference, )

    class Meta:
        abstract = True


class Interview(BaseInterview):

    potential_subject = models.ForeignKey(PotentialSubject)

    history = SyncHistoricalRecords()

    objects = InterviewManager()

    def __str__(self):
        return self.potential_subject.subject_identifier

    def natural_key(self):
        return (self.reference, )

    class Meta:
        app_label = 'bcpp_interview'
        get_latest_by = 'interview_datetime'
        verbose_name = 'In-depth Interview'
        unique_together = ('reference', 'potential_subject')


class GroupDiscussionLabel(SyncModelMixin, BaseUuidModel):

    discussion_label = models.CharField(
        max_length=50,
        unique=True)

    history = SyncHistoricalRecords()

    objects = GroupDiscussionLabelManager()

    def __str__(self):
        return self.discussion_label

    def natural_key(self):
        return (self.discussion_label, )

    class Meta:
        app_label = 'bcpp_interview'


class GroupDiscussion(BaseInterview):

    group_discussion_label = models.ForeignKey(
        to=GroupDiscussionLabel,
        verbose_name='Discussion Label')

    focus_group = models.ForeignKey(FocusGroup)

    comment = EncryptedTextField(
        verbose_name="Additional comment that may assist in analysis of this discussion",
        max_length=250,
        blank=True,
        null=True)

    history = SyncHistoricalRecords()

    objects = InterviewManager()

    def __str__(self):
        return self.focus_group.reference

    def natural_key(self):
        return (self.reference, )

    class Meta:
        app_label = 'bcpp_interview'
        get_latest_by = 'interview_datetime'
        verbose_name = 'Focus Group Discussion'


class InterviewRecording(SyncModelMixin, RecordingModelMixin, BaseUuidModel):

    interview = models.ForeignKey(Interview)

    verified = models.CharField(
        max_length=10,
        choices=YES_NO,
        default=NO,
        help_text='Indicate if the subject has agreed that this recording may be used for analysis')

    objects = RecordingManager()

    history = SyncHistoricalRecords()

    def natural_key(self):
        return (self.sound_filename, )

    class Meta:
        app_label = 'bcpp_interview'
        get_latest_by = 'start_datetime'
        verbose_name = 'In-depth Interview Recording'


class GroupDiscussionRecording(SyncModelMixin, RecordingModelMixin, BaseUuidModel):

    group_discussion = models.ForeignKey(GroupDiscussion)

    verified = models.CharField(
        max_length=10,
        choices=YES_NO,
        default=NO,
        help_text='Indicate if the group members have agreed that this recording may be used for analysis')

    history = SyncHistoricalRecords()

    objects = RecordingManager()

    def natural_key(self):
        return (self.sound_filename, )

    class Meta:
        app_label = 'bcpp_interview'
        get_latest_by = 'start_datetime'
        verbose_name = 'Focus Group Discussion Recording'


class SubjectLoss(SyncModelMixin, BaseUuidModel):

    potential_subject = models.ForeignKey(PotentialSubject)

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

    history = SyncHistoricalRecords()

    objects = SubjectLossManager()

    def __str__(self):
        return self.subject_identifier

    def save(self, *args, **kwargs):
        self.subject_identifier = self.potential_subject.subject_identifier
        self.registered_subject = self.potential_subject.registered_subject
        super(SubjectLoss, self).save(*args, **kwargs)

    def natural_key(self):
        return (self.subject_identifier, )

    class Meta:
        app_label = 'bcpp_interview'
        verbose_name_plural = "Subject Loss"


class SubjectLocation(MapperModelMixin, BaseUuidModel):

    subject_identifier = models.CharField(
        max_length=25,
        unique=True)

    community = models.CharField(
        max_length=25)

    objects = SubjectLocationManager()

    def __str__(self):
        return '{} {} (latitude={}, longitude={})'.format(
            self.subject_identifier, self.community, self.point.latitude, self.point.longitude)

    def natural_key(self):
        return (self.subject_identifier, )

    def save(self, *args, **kwargs):
        self.map_area = self.community.replace(' ', '_').lower()
        self.gps_target_lon = self.gps_confirm_longitude
        self.gps_target_lat = self.gps_confirm_latitude
        self.target_radius = 25
        super(SubjectLocation, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_interview'
        verbose_name_plural = "Subject Location"


class Survey(BaseUuidModel):
    """Dummy survey class for mappers."""

    name = models.CharField(
        max_length=10,
        null=True)

    class Meta:
        app_label = 'bcpp_interview'
        verbose_name_plural = "Survey"


class RawData(BaseUuidModel):

    subject_identifier = models.CharField(
        max_length=25,
        unique=True)

    identity = IdentityField(null=True)

    first_name = FirstnameField(null=True)

    last_name = LastnameField(null=True)

    pair = models.IntegerField(
        null=True)

    community = models.CharField(
        max_length=25,
        null=True)

    intervention = models.CharField(
        max_length=25,
        null=True)

    age_at_interview = models.CharField(
        max_length=25,
        null=True)

    gender = models.CharField(
        max_length=25,
        null=True)

    education = models.CharField(
        max_length=75,
        null=True)

    working = models.CharField(
        max_length=25,
        null=True)

    referral_appt_dt = models.CharField(
        max_length=25,
        null=True)

    cd4_value = models.CharField(
        max_length=25,
        null=True)

    viral_load = models.CharField(
        max_length=25,
        null=True)

    final_arv_Status = models.CharField(
        max_length=25,
        null=True)

    flag = models.CharField(
        max_length=50,
        null=True)

    art_eligible = models.CharField(
        max_length=25,
        null=True)

    art_eligible_natl = models.CharField(
        max_length=25,
        null=True)

    art_eligible_expanded = models.CharField(
        max_length=25,
        null=True)

    pims_registration_date = models.CharField(
        max_length=25,
        null=True)

    pims_art_initiation_date = models.CharField(
        max_length=25,
        null=True)

    pimsclinicname = models.CharField(
        max_length=25,
        null=True)

    first_arv = models.CharField(
        max_length=25,
        null=True)

    clinic_receiving_from = models.CharField(
        max_length=25,
        null=True)

    on_arv = models.CharField(
        max_length=25,
        null=True)

    why_no_arv = models.CharField(
        max_length=50,
        null=True)

    t1_visit_date = models.CharField(
        max_length=25,
        null=True)

    ref_code_t1 = models.CharField(
        max_length=25,
        null=True)

    issue = models.CharField(
        max_length=25,
        null=True)

    elig_cat = models.CharField(
        max_length=25,
        null=True)

    latitude = models.DecimalField(
        max_digits=15,
        null=True,
        decimal_places=10)

    longitude = models.DecimalField(
        max_digits=15,
        null=True,
        decimal_places=10)

    gender_plot = models.CharField(
        max_length=25,
        null=True)

    dob = models.CharField(
        max_length=25,
        null=True)

    clinic_receiving_from_t1 = models.CharField(
        max_length=50,
        null=True)

    on_arv_t1 = models.CharField(
        max_length=25,
        null=True)

    keepme = models.CharField(
        max_length=25,
        null=True)

    keepme_bhs = models.CharField(
        max_length=25,
        null=True)

    keepme_ahs = models.CharField(
        max_length=25,
        null=True)

    pims_reg_date = models.CharField(
        max_length=25,
        null=True)

    pims_art_date = models.CharField(
        max_length=25,
        null=True)

    currently_pregnant = models.CharField(
        max_length=25,
        null=True)

    visit_date_t0 = models.CharField(
        max_length=25,
        null=True)

    visit_date_t1 = models.CharField(
        max_length=25,
        null=True)

    ever_taken_arv_t1 = models.CharField(
        max_length=25,
        null=True)

    first_arv_t1 = models.CharField(
        max_length=25,
        null=True)

    post_t1_initiate = models.IntegerField(
        null=True)

    plot_identifier = models.CharField(
        max_length=25,
        null=True)

    post_t0_link = models.IntegerField(
        null=True)

    category = models.CharField(
        max_length=25,
        null=True)

    sub_category = models.CharField(
        max_length=25,
        null=True)

    source = models.CharField(
        max_length=25,
        null=True)

    def __str__(self):
        return self.subject_identifier

    class Meta:
        app_label = 'bcpp_interview'


@receiver(post_save, sender=SubjectConsent, dispatch_uid='post_save_consented')
def post_save_consented(sender, instance, raw, created, using, update_fields, **kwargs):
    if not raw:
        potential_subject = PotentialSubject.objects.get(identity=instance.identity)
        potential_subject.contacted = True
        potential_subject.consented = True
        potential_subject.save(
            update_fields=['contacted', 'consented', 'user_modified', 'modified'])


@receiver(post_save, sender=InterviewRecording, dispatch_uid='post_save_interview_recording')
def post_save_interview_recording(sender, instance, raw, created, using, update_fields, **kwargs):
    if not raw:
        instance.interview.potential_subject.interviewed = True
        instance.interview.potential_subject.idi = True
        instance.interview.potential_subject.save(update_fields=['interviewed', 'idi', 'user_modified', 'modified'])


@receiver(post_save, sender=GroupDiscussionRecording, dispatch_uid='post_save_group_discussion_recording')
def post_save_group_discussion_recording(sender, instance, raw, created, using, update_fields, **kwargs):
    if not raw:
        for obj in FocusGroupItem.objects.filter(
                focus_group=instance.group_discussion.focus_group):
            obj.potential_subject.interviewed = True
            obj.potential_subject.fgd = True
            obj.potential_subject.save(update_fields=['interviewed', 'fgd', 'user_modified', 'modified'])


@receiver(post_delete, sender=GroupDiscussionRecording, dispatch_uid='post_delete_group_discussion_recording')
def post_delete_group_discussion_recording(sender, instance, using, **kwargs):
    try:
        GroupDiscussionRecording.objects.get(group_discussion=instance.group_discussion)
    except GroupDiscussionRecording.DoesNotExist:
        for focus_group_item in FocusGroupItem.objects.filter(
                focus_group=instance.group_discussion.focus_group):
            focus_group_item.potential_subject.interviewed = False
            focus_group_item.potential_subject.fgd = False
            focus_group_item.potential_subject.save(update_fields=['fgd', 'modified'])
    except GroupDiscussionRecording.MultipleObjectsReturned:
        pass


@receiver(post_delete, sender=InterviewRecording, dispatch_uid='post_delete_interview_recording')
def post_delete_interview_recording(sender, instance, using, **kwargs):
    try:
        InterviewRecording.objects.get(interview=instance.interview)
    except InterviewRecording.DoesNotExist:
        for potential_subject in PotentialSubject.objects.filter(pk=instance.interview.potential_subject):
            potential_subject.interviewed = False
            potential_subject.idi = False
            potential_subject.save(update_fields=['idi', 'modified'])
    except InterviewRecording.MultipleObjectsReturned:
        pass
