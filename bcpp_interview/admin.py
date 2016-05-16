from django.contrib import admin

from edc_base.modeladmin.admin.base_tabular_inline import BaseTabularInline
from edc_consent.admin.mixins import ModelAdminConsentMixin

from edc_base.modeladmin.mixins import (
    ModelAdminModelRedirectMixin, ModelAdminChangelistModelButtonMixin,
    ModelAdminRedirectMixin, ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin,
    ModelAdminAuditFieldsMixin)

from .actions import record, create_subject_group, add_to_group_discussion
from .models import (
    SubjectGroup, Interview, GroupDiscussion, SubjectGroupItem, InterviewRecording,
    GroupDiscussionRecording, PotentialSubject, SubjectLoss, SubjectConsent)
from .forms import SubjectConsentForm
from bcpp_interview.models import GroupDiscussionLabel


class BaseModelAdmin(ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin,
                     ModelAdminAuditFieldsMixin, admin.ModelAdmin):
    list_per_page = 15
    date_hierarchy = 'created'


class ModelAdminPotentialSubjectRedirectMixin(ModelAdminModelRedirectMixin):

    additional_instructions = 'After saving you will be returned to the list of Potential Subjects.'
    redirect_app_label = 'bcpp_interview'
    redirect_model_name = 'potentialsubject'


@admin.register(SubjectConsent)
class SubjectConsentAdmin(ModelAdminConsentMixin,
                          ModelAdminPotentialSubjectRedirectMixin, BaseModelAdmin):

    remove_consent_fields = ['may_store_samples', 'study_site']

    redirect_search_field = 'subject_identifier'

    form = SubjectConsentForm


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
class SubjectGroupAdmin(ModelAdminChangelistModelButtonMixin, BaseModelAdmin):

    date_hierarchy = 'created'

    fields = [
        'group_name',
        'size',
        'category']

    list_display = ['group_name', 'category', 'discussion', 'created', 'user_created']

    search_fields = ['group_name', ]

    list_filter = ['category', 'created', 'user_created']

    inlines = [SubjectGroupItemInline]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(SubjectGroupAdmin, self).get_readonly_fields(request, obj)
        return list(readonly_fields) + ['group_name']

    def get_group_discussion_button(self, obj):
        reverse_args = None
        try:
            group_discussion = GroupDiscussion.objects.get(subject_group=obj)
            reverse_args = (group_discussion.pk, )
        except GroupDiscussion.DoesNotExist:
            pass
            reverse_args = None
        return self.changelist_model_button(
            'bcpp_interview', 'groupdiscussion', reverse_args=reverse_args,
            change_label='discussion', add_querystring='?subject_group={}'.format(obj.pk))

    def discussion(self, obj):
        return self.get_group_discussion_button(obj)
    discussion.short_description = 'discussion'
    discussion.allow_tags = True


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
            'label', 'start_datetime', 'stop_datetime', 'sound_filename',
            'sound_filesize', 'recording_time']


@admin.register(InterviewRecording)
class InterviewRecordingAdmin(BaseRecordingAdmin):

    def get_list_display(self, request):
        return ['interview'] + self.list_display


@admin.register(GroupDiscussionRecording)
class GroupDiscussionRecordingAdmin(BaseRecordingAdmin):

    def get_list_display(self, request):
        return ['group_discussion'] + self.list_display

    search_fields = ['label', 'sound_filename', 'group_discussion__subject_group__group_name']


class InterviewRecordingInline(BaseTabularInline):

    model = InterviewRecording
    extra = 0


class GroupDiscussionRecordingInline(BaseTabularInline):

    model = GroupDiscussionRecording
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(GroupDiscussionRecordingInline, self).get_readonly_fields(request, obj)
        return list(readonly_fields) + [
            'label', 'start_datetime', 'stop_datetime', 'sound_filename',
            'sound_filesize', 'recording_time']

    fields = [
        'label', 'verified', 'comment',
        'start_datetime', 'stop_datetime', 'sound_filename',
        'sound_filesize', 'recording_time']

    radio_fields = {
        'verified': admin.VERTICAL}


class BaseInterviewAdmin(BaseModelAdmin):

    date_hierarchy = 'interview_datetime'

    list_filter = ['interviewed', 'interview_datetime', 'created', 'user_created', ]

    actions = [record]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(BaseInterviewAdmin, self).get_readonly_fields(request, obj)
        return list(readonly_fields) + ['interview_name']


@admin.register(Interview)
class InterviewAdmin(ModelAdminPotentialSubjectRedirectMixin, BaseInterviewAdmin):

    redirect_search_field = 'potential_subject.subject_identifier'

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

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = list(self.readonly_fields or [])
        if obj:
            self.readonly_fields = list(self.fields)
            self.readonly_fields.remove('location')
        else:
            self.readonly_fields = []
        return tuple(self.readonly_fields)

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

    fields = [
        'interview_name',
        'group_discussion_label',
        'subject_group',
        'interview_datetime',
        'location']

    list_display = [
        'group_discussion_label',
        'subject_group',
        'interviewed',
        'created',
        'user_created',
    ]

    def get_list_filter(self, request):
        self.list_filter = list(super(GroupDiscussionAdmin, self).get_list_filter(request))
        if 'group_discussion_label' not in self.list_filter:
            self.list_filter = ['group_discussion_label'] + self.list_filter
        return tuple(self.list_filter)

    search_fields = [
        'subject_group__group_name',
        'subject_group__potential_subject__subject_consent__first_name',
        'subject_group__potential_subject__subject_consent__last_name',
        'subject_group__potential_subject__subject_consent__identity',
    ]

    inlines = [GroupDiscussionRecordingInline]


@admin.register(GroupDiscussionLabel)
class GroupDiscussionLabelAdmin(BaseModelAdmin):
    pass


@admin.register(PotentialSubject)
class PotentialSubjectAdmin(ModelAdminRedirectMixin, ModelAdminChangelistModelButtonMixin,
                            BaseModelAdmin):

    list_display = ['subject_identifier', 'identity', 'consent', 'interview', 'subject_group',
                    'consented', 'interviewed', 'ki', 'fgd',
                    'category', 'community', 'region']

    list_filter = ['consented', 'interviewed', 'category', 'ki', 'fgd', 'community', 'region']

    radio_fields = {
        'category': admin.VERTICAL,
        'region': admin.VERTICAL
    }

    search_fields = ['identity', 'subject_identifier', 'registered_subject__identity']

    readonly_fields = ['subject_identifier', 'identity', 'category', 'community', 'region']

    actions = [create_subject_group, add_to_group_discussion]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(PotentialSubjectAdmin, self).get_search_results(
            request, queryset, search_term)
        try:
            subject_group_items = SubjectGroupItem.objects.filter(
                subject_group__group_name__icontains=search_term)
            potential_subjects = [obj.potential_subject.pk for obj in subject_group_items]
            queryset |= self.model.objects.filter(pk__in=potential_subjects)
        except SubjectGroupItem.DoesNotExist:
            pass
        return queryset, use_distinct

    def consent(self, obj):
        reverse_args = None
        if obj.subject_consent:
            reverse_args = (obj.subject_consent.pk, )
        return self.changelist_model_button(
            'bcpp_interview', 'subjectconsent', reverse_args=reverse_args,
            change_label='consent')
    consent.short_description = 'Consent'
    consent.allow_tags = True

    def get_interview_button(self, obj):
        reverse_args = None
        querystring = None
        disabled = None
        try:
            SubjectGroupItem.objects.get(potential_subject=obj)
            return '-'
        except SubjectGroupItem.DoesNotExist:
            pass
        try:
            interview = Interview.objects.get(potential_subject=obj)
            reverse_args = (interview.pk, )
        except Interview.DoesNotExist:
            if obj.subject_consent:
                querystring = '?potential_subject=' + str(obj.pk)
            else:
                disabled = True
        return self.changelist_model_button(
            'bcpp_interview', 'interview', reverse_args=reverse_args,
            change_label='KI', add_querystring=querystring, disabled=disabled)

    def get_subject_group_button(self, obj):
        disabled = None
        change_label = 'FGD'
        querystring_value = None
        if not obj.subject_consent:
            return '-'
        try:
            Interview.objects.get(potential_subject=obj)
            return '-'
        except Interview.DoesNotExist:
            pass
        try:
            subject_group_item = SubjectGroupItem.objects.get(potential_subject=obj)
            subject_group = subject_group_item.subject_group
            change_label = subject_group.group_name
            querystring_value = str(subject_group.group_name)
        except SubjectGroupItem.DoesNotExist:
            return 'add'
        return self.changelist_list_button(
            'bcpp_interview', 'subjectgroup', label=change_label,
            querystring_value=querystring_value, disabled=disabled)

    def interview(self, obj):
        return self.get_interview_button(obj)
    interview.short_description = 'interview'
    interview.allow_tags = True

    def subject_group(self, obj):
        return self.get_subject_group_button(obj)
    subject_group.short_description = 'subject group'
    subject_group.allow_tags = True


@admin.register(SubjectLoss)
class SubjectLossAdmin(BaseModelAdmin):

    date_hierarchy = 'report_datetime'

    fields = ['potential_subject', 'report_datetime', 'reason', 'reason_other']

    list_display = ['subject_identifier', 'reason']

    list_filter = ['reason', 'report_datetime']

    radio_fields = {'reason': admin.VERTICAL}

    search_fields = ['subject_identifier', 'registered_subject__identity']
