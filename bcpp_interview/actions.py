from django.contrib import messages
from django.http.response import HttpResponseRedirect
from bcpp_interview.models import Interview, SubjectGroupItem, SubjectGroup
from django.core.urlresolvers import reverse


def record(modeladmin, request, queryset):
    if queryset.count() != 1:
        messages.warning(request, "Select only ONE interview or group discussion to record.")
        return None
    obj = queryset[0]
    return HttpResponseRedirect("/record/{}/{}/{}/".format(
        obj._meta.app_label, obj._meta.model_name, obj.pk))
record.short_description = "Start Recording Interview"


def verify_available_for_subject_group(request, potential_subject, category):
    warning = None
    if not potential_subject.subject_consent:
        messages.warning(
            request, "Some subjects have not consented. See {}".format(potential_subject))
        warning = True
    if not warning and potential_subject.category != category:
        messages.warning(
            request, "All subjects must be in the same category. Got \'{} {} {}\' not in category \'{}\'".format(
                potential_subject.subject_identifier, potential_subject.subject_consent.first_name, potential_subject.subject_consent.last_name, category))
        warning = True
    if not warning and potential_subject.interviewed:
        messages.warning(
            request, "Some subjects have already been interviewed. See {}".format(potential_subject))
        warning = True
    if not warning:
        try:
            Interview.objects.get(potential_subject=potential_subject)
            messages.warning(
                request, "Some subjects are setup for a Interview. See {}".format(potential_subject))
            warning = True
        except Interview.DoesNotExist:
            pass
    if not warning:
        try:
            subject_group_item = SubjectGroupItem.objects.get(potential_subject=potential_subject)
            messages.warning(
                request, "Some subjects are already in a group discussion. See {} and subject group {}".format(
                    potential_subject, subject_group_item.subject_group))
            warning = True
        except SubjectGroupItem.DoesNotExist:
            pass
    return request, warning


def add_to_group_discussion(modeladmin, request, queryset):
    subject_groups = []
    potential_subjects = []
    warning = None
    category = None
    for obj in queryset:
        try:
            subject_group_item = SubjectGroupItem.objects.get(potential_subject=obj)
            subject_groups.append(subject_group_item.subject_group)
            category = subject_group_item.potential_subject.category
        except SubjectGroupItem.DoesNotExist:
            potential_subjects.append(obj)
    group_name = list(set([obj.group_name for obj in subject_groups]))
    if len(group_name) > 1:
        messages.warning(
            request,
            "Subjects were selected from multiple groups. Select subjects from one of {}".format(', '.join(group_name)))
    elif len(group_name) == 0:
        messages.warning(
            request, "At least one selected subject must be in a subject group")
    elif len(potential_subjects) == 0:
        messages.warning(
            request, "Select at least one subject to add to group {}".format(group_name[0]))
    else:
        group_name = group_name[0]
        for obj in potential_subjects:
            request, warning = verify_available_for_subject_group(
                request, potential_subject=obj, category=category)
            if warning:
                break
        if not warning:
            for obj in potential_subjects:
                SubjectGroupItem.objects.create(
                    subject_group=subject_groups[0],
                    potential_subject=obj)
            messages.success(
                request, "{} subjects were successfully added to subject group {}".format(
                    len(potential_subjects), group_name))
    url = reverse(
        'admin:bcpp_interview_potentialsubject_changelist')
    return HttpResponseRedirect(url)
add_to_group_discussion.short_description = "Add to existing Group Discussion"


def create_subject_group(modeladmin, request, queryset):
    # confirm all consented
    warning = False
    category = None
    if queryset.count() < 2:
        messages.warning(
            request, "A subject group must have at least 8 subjects. Got {}".format(queryset.count()))
        warning = True
    for obj in queryset:
        if not category:
            category = obj.category
        request, warning = verify_available_for_subject_group(potential_subject=obj)
    if not warning:
        subject_group = SubjectGroup.objects.create(
            size=queryset.count(),
            category=obj.category)
        for obj in queryset:
            SubjectGroupItem.objects.create(
                subject_group=subject_group,
                potential_subject=obj)
            messages.warning(
                request, "Subject Group \'{}\' was successfully created.".format(subject_group.group_name))
    url = reverse(
        'admin:bcpp_interview_potentialsubject_changelist') + (
            '?category__exact={}&consented__exact=1&interviewed__exact=0').format(category)
    return HttpResponseRedirect(url)
create_subject_group.short_description = "Create Subject Group"
