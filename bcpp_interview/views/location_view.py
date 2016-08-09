import json

from django.apps import apps as django_apps
from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse

from edc_base.views import EdcBaseViewMixin
from edc_map.views import MapImageView

from ..models import SubjectLocation


class LocationView(EdcBaseViewMixin, MapImageView):

    item_model = SubjectLocation
    item_model_field = 'subject_identifier'
    filename_field = 'subject_identifier'
    zoom_levels = django_apps.get_app_config('edc_map').zoom_levels

    def get_context_data(self, **kwargs):
        context = super(LocationView, self).get_context_data(**kwargs)
        context.update(
            site_header=admin.site.site_header,
            back_subject_url=reverse(
                'admin:bcpp_interview_potentialsubject_changelist') +
            '?q=' + self.kwargs.get('subject_identifier'),
            back_call_url=reverse(
                'edc_call_manager_admin:call_manager_call_changelist') +
            '?q=' + self.kwargs.get('subject_identifier'),
            add_point_url=reverse('admin:bcpp_interview_subjectlocation_add')
        )
        # add new items to the json_data object
        data = dict(
            back_subject_url=context['back_subject_url'],
            back_call_url=context['back_call_url'],
            add_point_url=context['add_point_url'],
            **json.loads(context['json_data']))
        json_data = json.dumps(data, cls=DjangoJSONEncoder)
        context.update(json_data=json_data)
        return context
