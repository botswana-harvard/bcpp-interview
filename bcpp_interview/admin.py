from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from edc_base.modeladmin.admin.base_tabular_inline import BaseTabularInline
from edc_base.modeladmin.mixins import (
    ModelAdminModelRedirectMixin, ModelAdminChangelistModelButtonMixin,
    ModelAdminRedirectMixin, ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin,
    ModelAdminAuditFieldsMixin)
from edc_consent.admin.mixins import ModelAdminConsentMixin

from .actions import record, create_focus_group, add_to_focus_group_discussion
from .forms import SubjectConsentForm
from .models import (
    FocusGroup, Interview, GroupDiscussion, FocusGroupItem, InterviewRecording,
    GroupDiscussionRecording, PotentialSubject, SubjectLoss, SubjectConsent,
    GroupDiscussionLabel)


class RecordingAdminSite(AdminSite):
    site_header = 'BCPP Interview'
    site_title = 'BCPP Recordings'
    index_title = 'BCPP Recordings Admin'
    site_url = '/recording/bcpp_interview/'
    # app_index_template = settings.

recording_admin = RecordingAdminSite(name='recordings')


class BaseModelAdmin(ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin,
                     ModelAdminAuditFieldsMixin, admin.ModelAdmin):
    list_per_page = 10
    date_hierarchy = 'created'
    empty_value_display = '-'


class ModelAdminPotentialSubjectRedirectMixin(ModelAdminModelRedirectMixin):

    additional_instructions = 'After saving you will be returned to the list of Potential Subjects.'
    redirect_app_label = 'bcpp_interview'
    redirect_model_name = 'potentialsubject'


class ModelAdminAudioPlaybackMixin(object):

    def play(self, obj):
        kwargs = {'app_label': obj._meta.app_label, 'model_name': obj._meta.model_name, 'pk': obj.pk}
        url = reverse('play', kwargs=kwargs)
        return format_html(
            '<button id="play-{id}" onclick="return startPlayback(\'{id}\', \'{url}\');" '
            'class="button">Play</button>', id=obj.pk, url=url)
    play.short_description = 'Play'

    def stop(self, obj):
        kwargs = {'app_label': obj._meta.app_label, 'model_name': obj._meta.model_name, 'pk': obj.pk}
        url = reverse('play', kwargs=kwargs)
        return format_html(
            '<button id="stop-{id}" onclick="return stopPlayback(\'{id}\', \'{url}\');" '
            'class="button">Stop</button>', id=obj.pk, url=url)
    stop.short_description = 'Stop'

    def record(self, obj):
        kwargs = {'app_label': obj._meta.app_label, 'model_name': obj._meta.model_name, 'pk': obj.pk}
        url = reverse('record', kwargs=kwargs)
        print(url)
        return format_html(
            '<a id="record-{id}" href="{url}" '
            'class="button">Record</a>', id=obj.pk, url=url)
    record.short_description = 'record'


@admin.register(SubjectConsent)
class SubjectConsentAdmin(ModelAdminConsentMixin,
                          ModelAdminPotentialSubjectRedirectMixin, BaseModelAdmin):

    remove_consent_fields = ['may_store_samples', 'study_site']

    redirect_search_field = 'subject_identifier'

    form = SubjectConsentForm


@admin.register(FocusGroupItem)
class FocusGroupItemAdmin(BaseModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "potential_subject":
            try:
                potential_subject = PotentialSubject.objects.filter(consented=True, idi=False)
            except PotentialSubject.DoesNotExist:
                potential_subject = PotentialSubject.objects.none()
            kwargs["queryset"] = potential_subject
        return super(FocusGroupItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class FocusGroupItemInline(BaseTabularInline):
    model = FocusGroupItem
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "potential_subject":
            try:
                potential_subject = PotentialSubject.objects.filter(consented=True, idi=False)
            except PotentialSubject.DoesNotExist:
                potential_subject = PotentialSubject.objects.none()
            kwargs["queryset"] = potential_subject
        return super(FocusGroupItemInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(FocusGroup)
class FocusGroupAdmin(ModelAdminChangelistModelButtonMixin, BaseModelAdmin):

    date_hierarchy = 'created'

    fields = [
        'reference',
        'size',
        'category']

    list_display = ['reference', 'category', 'sub_category', 'discussion', 'potential_subject_button',
                    'created', 'user_created']

    search_fields = ['reference', ]

    list_filter = ['category', 'sub_category', 'created', 'user_created']

    inlines = [FocusGroupItemInline]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(FocusGroupAdmin, self).get_readonly_fields(request, obj)
        return list(readonly_fields) + ['reference']

    def get_group_discussion_button(self, obj):
        try:
            group_discussion = GroupDiscussion.objects.get(focus_group=obj)
            group_discussion_button = self.changelist_list_button(
                'bcpp_interview', 'groupdiscussion',
                label=group_discussion.reference, querystring_value=group_discussion.focus_group.reference)
        except GroupDiscussion.DoesNotExist:
            group_discussion_button = self.changelist_model_button(
                'bcpp_interview', 'groupdiscussion',
                change_label='discussion', add_querystring='?focus_group={}'.format(obj.pk))
        return group_discussion_button

    def discussion(self, obj):
        return self.get_group_discussion_button(obj)
    discussion.short_description = 'discussion'

    def potential_subject_button(self, obj):
        return self.changelist_list_button(
            'bcpp_interview', 'potentialsubject', label='subjects',
            querystring_value=obj.reference)
    potential_subject_button.short_description = 'subjects'


class BaseRecordingAdmin(ModelAdminAudioPlaybackMixin, ModelAdminChangelistModelButtonMixin, BaseModelAdmin):

    date_hierarchy = 'start_datetime'

    list_per_page = 5

    fields = [
        'label', 'verified', 'comment',
        'start_datetime', 'stop_datetime', 'sound_filename',
        'sound_filesize', 'recording_time']

    radio_fields = {'verified': admin.VERTICAL}

    list_display = ['label', 'play', 'stop', 'verified', 'played', 'recording_time', 'filesize',
                    'start_datetime', 'stop_datetime', ]

    list_filter = ['verified', 'played', 'start_datetime']

    search_fields = ['label', 'sound_filename']

    ordering = ('-start_datetime', )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(BaseRecordingAdmin, self).get_readonly_fields(request, obj)
        return list(readonly_fields) + [
            'label', 'start_datetime', 'stop_datetime', 'sound_filename',
            'sound_filesize', 'recording_time']


class InterviewRecordingAdmin(BaseRecordingAdmin):

    def get_list_display(self, request):
        self.list_display = list(self.list_display)
        if 'interview_button' not in self.list_display:
            self.list_display.insert(1, 'interview_button')
        return tuple(self.list_display)

    def interview_button(self, obj):
        return self.get_interview_button(obj)
    interview_button.short_description = 'interview'

    def get_interview_button(self, obj):
        return self.changelist_list_button(
            'bcpp_interview', 'interview', label=obj.interview.reference,
            querystring_value=obj.interview.reference)

recording_admin.register(InterviewRecording, InterviewRecordingAdmin)


class GroupDiscussionRecordingAdmin(BaseRecordingAdmin):

    def get_list_display(self, request):
        self.list_display = list(self.list_display)
        if 'discussion_button' not in self.list_display:
            self.list_display.insert(1, 'discussion_button')
        return tuple(self.list_display)

    search_fields = ['label', 'sound_filename', 'group_discussion__focus_group__reference']

    def discussion_button(self, obj):
        return self.get_discussion_button(obj)
    discussion_button.short_description = 'discussion'

    def get_discussion_button(self, obj):
        return self.changelist_list_button(
            'bcpp_interview', 'groupdiscussion', label=obj.group_discussion.focus_group.reference,
            querystring_value=obj.group_discussion.focus_group.reference)

recording_admin.register(GroupDiscussionRecording, GroupDiscussionRecordingAdmin)


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


class BaseInterviewAdmin(ModelAdminAudioPlaybackMixin, ModelAdminChangelistModelButtonMixin, BaseModelAdmin):

    date_hierarchy = 'interview_datetime'

    list_filter = ['interviewed', 'interview_datetime', 'created', 'user_created', ]

    actions = [record]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(BaseInterviewAdmin, self).get_readonly_fields(request, obj)
        return list(readonly_fields) + ['reference']


@admin.register(Interview)
class InterviewAdmin(BaseInterviewAdmin):

    fields = [
        'reference',
        'interview_datetime',
        'potential_subject',
        'location',
    ]

    list_display = [
        'reference',
        'record',
        'playback_button',
        'potential_subject_button',
        'category',
        'interviewed',
        'created',
        'user_created',
    ]

    search_fields = [
        'reference',
        'potential_subject__subject_consent__first_name',
        'potential_subject__subject_consent__last_name',
        'potential_subject__subject_consent__identity',
    ]

    def category(self, obj):
        return obj.potential_subject.get_category_display()

    def potential_subject_button(self, obj):
        return self.changelist_list_button(
            'bcpp_interview', 'potentialsubject', label=obj.potential_subject.subject_identifier,
            querystring_value=obj.potential_subject.subject_identifier)
    potential_subject_button.short_description = 'subject'

    def playback_button(self, obj):
        count = InterviewRecording.objects.filter(interview__reference=obj.reference).count()
        if count == 0:
            return self.empty_value_display
        return self.changelist_list_button(
            'bcpp_interview', 'interviewrecording', label='{}-recordings'.format(count),
            querystring_value=obj.reference, namespace="recordings",
            title='2 recordings exist for this discussion')
    playback_button.short_description = 'Playback'

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
                potential_subject = PotentialSubject.objects.filter(
                    consented=True, idi=False,
                    pk=request.GET.get('potential_subject'))
            except PotentialSubject.DoesNotExist:
                try:
                    potential_subject = PotentialSubject.objects.filter(consented=True, idi=False)
                except PotentialSubject.DoesNotExist:
                    potential_subject = PotentialSubject.objects.none()
            kwargs["queryset"] = potential_subject
        return super(InterviewAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(GroupDiscussion)
class GroupDiscussionAdmin(BaseInterviewAdmin):

    fields = [
        'reference',
        'group_discussion_label',
        'focus_group',
        'interview_datetime',
        'location']

    list_display = [
        'reference',
        'group_discussion_label',
        'record',
        'playback',
        'focus_group_button',
        'interviewed',
        'created',
        'user_created',
    ]

    search_fields = ('reference', 'group_discussion_label__discussion_label', 'focus_group__reference')

    def focus_group_button(self, obj):
        return self.changelist_list_button(
            'bcpp_interview', 'focusgroup', label=obj.focus_group.reference,
            querystring_value=obj.focus_group.reference)
    focus_group_button.short_description = 'focus-group'

    def playback(self, obj):
        count = GroupDiscussionRecording.objects.filter(group_discussion__reference=obj.reference).count()
        if count == 0:
            return self.empty_value_display
        return self.changelist_list_button(
            'bcpp_interview', 'groupdiscussionrecording', label='{}-recordings'.format(count),
            querystring_value=obj.reference, namespace="recordings",
            title='2 recordings exist for this discussion')
    playback.short_description = 'Playback'

    def get_list_filter(self, request):
        self.list_filter = list(super(GroupDiscussionAdmin, self).get_list_filter(request))
        if 'group_discussion_label' not in self.list_filter:
            self.list_filter = ['group_discussion_label'] + self.list_filter
        return tuple(self.list_filter)


@admin.register(GroupDiscussionLabel)
class GroupDiscussionLabelAdmin(BaseModelAdmin):
    pass


@admin.register(PotentialSubject)
class PotentialSubjectAdmin(ModelAdminRedirectMixin, ModelAdminChangelistModelButtonMixin,
                            BaseModelAdmin):

    list_display = ['subject_identifier', 'identity', 'consent_button', 'in_depth_button',
                    'focus_group_button', 'consented', 'interviewed', 'idi', 'fgd',
                    'category', 'sub_category', 'community', 'region']

    list_filter = ['consented', 'interviewed', 'category', 'sub_category', 'idi', 'fgd', 'community', 'region']

    radio_fields = {
        'category': admin.VERTICAL,
        'sub_category': admin.VERTICAL,
        'region': admin.VERTICAL
    }

    search_fields = ['identity', 'subject_identifier', 'registered_subject__identity']

    readonly_fields = ['subject_identifier', 'identity', 'category', 'sub_category', 'community', 'region']

    actions = [create_focus_group, add_to_focus_group_discussion]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(PotentialSubjectAdmin, self).get_search_results(
            request, queryset, search_term)
        try:
            focus_group_items = FocusGroupItem.objects.filter(
                focus_group__reference__icontains=search_term)
            potential_subjects = [obj.potential_subject.pk for obj in focus_group_items]
            queryset |= self.model.objects.filter(pk__in=potential_subjects)
        except FocusGroupItem.DoesNotExist:
            pass
        return queryset, use_distinct

    def consent_button(self, obj):
        reverse_args = None
        if obj.subject_consent:
            reverse_args = (obj.subject_consent.pk, )
        return self.changelist_model_button(
            'bcpp_interview', 'subjectconsent', reverse_args=reverse_args,
            change_label='consent')
    consent_button.short_description = 'Consent'

    def get_in_depth_button(self, obj):
        disabled = None
        try:
            FocusGroupItem.objects.get(potential_subject=obj)
            return self.empty_value_display
        except FocusGroupItem.DoesNotExist:
            pass
        try:
            interview = Interview.objects.get(potential_subject=obj)
            interview_button = self.changelist_list_button(
                'bcpp_interview', 'interview', label=interview.reference,
                querystring_value=interview.reference, disabled=disabled)
        except Interview.DoesNotExist:
            if not obj.subject_consent:
                disabled = True
            interview_button = self.changelist_model_button(
                'bcpp_interview', 'interview', add_label='IDI',
                add_querystring='?potential_subject={}'.format(obj.pk),
                disabled=disabled, title='Add an in-depth interview for this subject')
        return interview_button

    def get_focus_group_button(self, obj):
        disabled = None
        change_label = 'FGD'
        querystring_value = None
        if not obj.subject_consent:
            return self.empty_value_display
        try:
            Interview.objects.get(potential_subject=obj)
            return self.empty_value_display
        except Interview.DoesNotExist:
            pass
        try:
            focus_group_item = FocusGroupItem.objects.get(potential_subject=obj)
            focus_group = focus_group_item.focus_group
            change_label = focus_group.reference
            querystring_value = str(focus_group.reference)
        except FocusGroupItem.DoesNotExist:
            return 'add'
        return self.changelist_list_button(
            'bcpp_interview', 'focusgroup', label=change_label,
            querystring_value=querystring_value, disabled=disabled)

    def in_depth_button(self, obj):
        return self.get_in_depth_button(obj)
    in_depth_button.short_description = 'in-depth'

    def focus_group_button(self, obj):
        return self.get_focus_group_button(obj)
    focus_group_button.short_description = 'focus-group'


@admin.register(SubjectLoss)
class SubjectLossAdmin(BaseModelAdmin):

    date_hierarchy = 'report_datetime'

    fields = ['potential_subject', 'report_datetime', 'reason', 'reason_other']

    list_display = ['subject_identifier', 'reason']

    list_filter = ['reason', 'report_datetime']

    radio_fields = {'reason': admin.VERTICAL}

    search_fields = ['subject_identifier', 'registered_subject__identity']
