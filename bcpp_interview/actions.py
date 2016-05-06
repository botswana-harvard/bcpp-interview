from django.contrib import messages
from django.http.response import HttpResponseRedirect


def record(modeladmin, request, queryset):
    if queryset.count() != 1:
        messages.warning(request, "Select only ONE interview or group discussion to record.")
        return None
    obj = queryset[0]
    return HttpResponseRedirect("/record/{}/".format(obj.interview_name))
record.short_description = "Start Recording Interview"
