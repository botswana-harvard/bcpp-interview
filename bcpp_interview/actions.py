from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect

from .models import Interview, FocusGroupItem, FocusGroup


def verify_available_for_focus_group(request, potential_subject, category):
    warning = None
    if not potential_subject.subject_consent:
        messages.error(
            request, "Some subjects have not consented. See {}".format(potential_subject))
        warning = True
    if not warning and potential_subject.category != category:
        messages.error(
            request, "All subjects must be in the same category. Got \'{} {} {}\' not in category \'{}\'".format(
                potential_subject.subject_identifier, potential_subject.subject_consent.first_name,
                potential_subject.subject_consent.last_name, category))
        warning = True
    if not warning and potential_subject.interviewed:
        messages.error(
            request, ('Some selected subjects have already been interviewed. '
                      'Subjects may not be interviewed more than once.').format(potential_subject))
        warning = True
    if not warning:
        try:
            Interview.objects.get(potential_subject=potential_subject)
            messages.error(
                request, ("Some subjects are already setup for an in-depth "
                          "interview. See {}").format(potential_subject))
            warning = True
        except Interview.DoesNotExist:
            pass
    if not warning:
        try:
            focus_group_item = FocusGroupItem.objects.get(potential_subject=potential_subject)
            messages.error(
                request, "Some subjects are already in a focus group. See {} of focus group {}".format(
                    potential_subject, focus_group_item.focus_group))
            warning = True
        except FocusGroupItem.DoesNotExist:
            pass
    return request, warning


def add_to_focus_group_discussion(modeladmin, request, queryset):
    focus_groups = []
    potential_subjects = []
    warning = None
    category = None
    for obj in queryset:
        try:
            focus_group_item = FocusGroupItem.objects.get(potential_subject=obj)
            focus_groups.append(focus_group_item.focus_group)
            category = focus_group_item.potential_subject.category
        except FocusGroupItem.DoesNotExist:
            potential_subjects.append(obj)
    reference = list(set([obj.reference for obj in focus_groups]))
    if len(reference) > 1:
        messages.error(
            request,
            ("Subjects were selected from multiple focus groups. Select "
             "subjects from one of {}").format(', '.join(reference)))
    elif len(reference) == 0:
        messages.error(
            request, "At least one selected subject must be in an \'existing\' focus group")
    elif len(potential_subjects) == 0:
        messages.error(
            request, "Select at least one subject to add to focus group {}".format(reference[0]))
    else:
        reference = reference[0]
        for obj in potential_subjects:
            request, warning = verify_available_for_focus_group(
                request, potential_subject=obj, category=category)
            if warning:
                break
        if not warning:
            for obj in potential_subjects:
                FocusGroupItem.objects.create(
                    focus_group=focus_groups[0],
                    potential_subject=obj)
            messages.success(
                request, "{} subjects were successfully added to focus group {}".format(
                    len(potential_subjects), reference))
    url = reverse(
        'admin:bcpp_interview_potentialsubject_changelist') + (
            '?q={}').format(reference)
    return HttpResponseRedirect(url)
add_to_focus_group_discussion.short_description = "Add to existing Focus Group"


def create_focus_group(modeladmin, request, queryset):
    """Create a focus group and include the potential subjects in the queryset."""
    warning = False
    category = None
    url = reverse(
        'admin:bcpp_interview_potentialsubject_changelist')
    if queryset.count() < 2:
        messages.error(
            request, "A focus group must have at least 2 subjects. Got {}".format(queryset.count()))
    else:
        for obj in queryset:
            if not category:
                category = obj.category
            request, warning = verify_available_for_focus_group(request, potential_subject=obj, category=category)
            if warning:
                break
        if not warning:
            focus_group = FocusGroup.objects.create(
                size=queryset.count(),
                category=obj.category)
            for index, obj in enumerate(queryset):
                FocusGroupItem.objects.create(
                    focus_group=focus_group,
                    potential_subject=obj)
            messages.success(
                request, "Focus Group \'{}\' with {} {} subjects was successfully created.".format(
                    focus_group.reference, focus_group.category, index + 1))
            url = reverse(
                'admin:bcpp_interview_potentialsubject_changelist') + (
                    '?q={}').format(focus_group.reference)
    return HttpResponseRedirect(url)
create_focus_group.short_description = "Create Focus Group"
