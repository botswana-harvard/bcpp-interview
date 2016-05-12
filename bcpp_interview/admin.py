from django.contrib import admin


from .models import SubjectConsent
from .forms import SubjectConsentForm
from edc_consent.admin import BaseConsentModelAdmin
from bcpp_interview.models import SubjectGroup, Interview, GroupDiscussion, SubjectGroupItem, InterviewRecording,\
    GroupDiscussionRecording, PotentialSubject, SubjectLoss
from edc_base.modeladmin.admin.base_model_admin import BaseModelAdmin
from edc_base.modeladmin.admin.base_tabular_inline import BaseTabularInline
from edc_consent.actions import flag_as_verified_against_paper, unflag_as_verified_against_paper
from bcpp_interview.actions import record


@admin.register(SubjectConsent)
class SubjectConsentAdmin(BaseConsentModelAdmin):

    form = SubjectConsentForm

    date_hierarchy = 'consent_datetime'

    list_display = [
        'subject_identifier', 'is_verified', 'is_verified_datetime', 'first_name',
        'initials', 'gender', 'dob', 'consent_datetime', 'created', 'modified',
        'user_created', 'user_modified']
    search_fields = ['id', 'subject_identifier', 'first_name', 'last_name', 'identity']

    actions = [flag_as_verified_against_paper, unflag_as_verified_against_paper]

    list_filter = [
        'gender',
        'is_verified',
        'is_verified_datetime',
        'language',
        'is_literate',
        'consent_datetime',
        'created',
        'modified',
        'user_created',
        'user_modified',
        'hostname_created']
    fields = [
        'subject_identifier',
        'first_name',
        'last_name',
        'initials',
        'language',
        'is_literate',
        'witness_name',
        'consent_datetime',
        'gender',
        'dob',
        'guardian_name',
        'is_dob_estimated',
        'identity',
        'identity_type',
        'confirm_identity',
        'is_incarcerated',
        'comment',
        'consent_reviewed',
        'study_questions',
        'assessment_score',
        'consent_copy']

    radio_fields = {
        "language": admin.VERTICAL,
        "gender": admin.VERTICAL,
        # "study_site": admin.VERTICAL,
        "is_dob_estimated": admin.VERTICAL,
        "identity_type": admin.VERTICAL,
        "is_incarcerated": admin.VERTICAL,
        "consent_reviewed": admin.VERTICAL,
        "study_questions": admin.VERTICAL,
        "assessment_score": admin.VERTICAL,
        "consent_copy": admin.VERTICAL,
        "is_literate": admin.VERTICAL}

    # override to disallow subject to be changed
    def get_readonly_fields(self, request, obj=None):
        super(BaseConsentModelAdmin, self).get_readonly_fields(request, obj)
        if obj:  # In edit mode
            return (
                'subject_identifier',
                'subject_identifier_as_pk',
                'study_site',
                'consent_datetime',) + self.readonly_fields
        else:
            return ('subject_identifier', 'subject_identifier_as_pk',) + self.readonly_fields


@admin.register(SubjectGroupItem)
class SubjectGroupItemAdmin(BaseModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "potential_subject":
            try:
                potential_subject = PotentialSubject.objects.filter(consented=True, ki=False)
            except PotentialSubject.DoesNotExist:
                potential_subject = PotentialSubject.objects.none()
            kwargs["queryset"] = potential_subject
        return super(SubjectGroupItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class SubjectGroupItemInline(BaseTabularInline):
    model = SubjectGroupItem
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "potential_subject":
            try:
                potential_subject = PotentialSubject.objects.filter(consented=True, ki=False)
            except PotentialSubject.DoesNotExist:
                potential_subject = PotentialSubject.objects.none()
            kwargs["queryset"] = potential_subject
        return super(SubjectGroupItemInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(SubjectGroup)
class SubjectGroupAdmin(BaseModelAdmin):

    date_hierarchy = 'created'

    fields = [
        'group_name',
        'size',
        'category']

    list_display = ['group_name', 'category', 'created', 'user_created']

    search_fields = ['group_name', ]

    list_filter = ['category', 'created', 'user_created']

    inlines = [SubjectGroupItemInline]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(SubjectGroupAdmin, self).get_readonly_fields(request, obj)
        return list(readonly_fields) + ['group_name']


class BaseRecordingAdmin(BaseModelAdmin):

    date_hierarchy = 'start_datetime'

    fields = [
        'label', 'verified', 'comment',
        'start_datetime', 'stop_datetime', 'sound_filename',
        'sound_filesize', 'recording_time']

    list_display = ['label', 'verified', 'start_datetime', 'stop_datetime', 'recording_time']

    list_filter = ['verified', 'start_datetime']

    search_fields = ['label', 'sound_filename']

    radio_fields = {
        'verified': admin.VERTICAL}

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(BaseRecordingAdmin, self).get_readonly_fields(request, obj)
        return list(readonly_fields) + [
            'start_datetime', 'stop_datetime', 'sound_filename',
            'sound_filesize', 'recording_time']


@admin.register(InterviewRecording)
class InterviewRecordingAdmin(BaseRecordingAdmin):

    def get_list_display(self, request):
        return ['interview'] + self.list_display


@admin.register(GroupDiscussionRecording)
class GroupDiscussionRecordingAdmin(BaseRecordingAdmin):

    def get_list_display(self, request):
        return ['group_discussion'] + self.list_display


class InterviewRecordingInline(BaseTabularInline):

    model = InterviewRecording
    extra = 0


class GroupDiscussionInline(BaseTabularInline):

    model = GroupDiscussionRecording
    extra = 0


class BaseInterviewAdmin(BaseModelAdmin):

    date_hierarchy = 'interview_datetime'

    list_filter = ['interviewed', 'interview_datetime', 'created', 'user_created', ]

    actions = [record]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(BaseInterviewAdmin, self).get_readonly_fields(request, obj)
        return list(readonly_fields) + ['interview_name']


@admin.register(Interview)
class InterviewAdmin(BaseInterviewAdmin):

    fields = [
        'interview_name',
        'interview_datetime',
        'potential_subject',
        'location',
    ]

    list_display = [
        'interview_name',
        'potential_subject',
        'interviewed',
        'created',
        'user_created',
    ]

    search_fields = [
        'interview_name',
        'potential_subject__subject_consent__first_name',
        'potential_subject__subject_consent__last_name',
        'potential_subject__subject_consent__identity',
    ]

    inlines = [InterviewRecordingInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "potential_subject":
            try:
                potential_subject = PotentialSubject.objects.filter(consented=True, ki=False)
            except PotentialSubject.DoesNotExist:
                potential_subject = PotentialSubject.objects.none()
            kwargs["queryset"] = potential_subject
        return super(InterviewAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(GroupDiscussion)
class GroupDiscussionAdmin(BaseInterviewAdmin):

    list_display = [
        'subject_group',
        'interviewed',
        'created',
        'user_created',
    ]

    search_fields = [
        'subject_group__group_name',
        'subject_group__potential_subject__subject_consent__first_name',
        'subject_group__potential_subject__subject_consent__last_name',
        'subject_group__potential_subject__subject_consent__identity',
    ]

    inlines = [GroupDiscussionInline]


@admin.register(PotentialSubject)
class PotentialSubjectAdmin(BaseModelAdmin):

    list_display = ['subject_identifier', 'identity', 'consent',
                    'consented', 'interviewed', 'ki', 'fgd',
                    'category', 'community', 'region']

    list_filter = ['consented', 'interviewed', 'ki', 'fgd', 'category', 'community', 'region']

    radio_fields = {
        'category': admin.VERTICAL,
        'region': admin.VERTICAL
    }

    search_fields = ['identity', 'subject_identifier', 'registered_subject__identity']

    readonly_fields = ['subject_identifier', 'identity', 'category', 'community', 'region']


@admin.register(SubjectLoss)
class SubjectLossAdmin(BaseModelAdmin):

    date_hierarchy = 'report_datetime'

    fields = ['potential_subject', 'report_datetime', 'reason', 'reason_other']

    list_display = ['subject_identifier', 'reason']

    list_filter = ['reason', 'report_datetime']

    radio_fields = {'reason': admin.VERTICAL}

    search_fields = ['subject_identifier', 'registered_subject__identity']
