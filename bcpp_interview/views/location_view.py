import json
from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse

from edc_map.views import MapImageView

from ..models import SubjectLocation
from django.core.serializers.json import DjangoJSONEncoder


class LocationView(MapImageView):

    item_model = SubjectLocation
    item_model_field = 'subject_identifier'
    app_label = 'bcpp_map'
    filename_field = 'subject_identifier'
    zoom_levels = ['14', '15', '16', '17', '18']

    def get_context_data(self, **kwargs):
        context = super(LocationView, self).get_context_data(**kwargs)
        context.update(
            title=settings.PROJECT_TITLE,
            project_name=settings.PROJECT_TITLE,
            site_header=admin.site.site_header,
            back_subject_url=reverse(
                'admin:bcpp_interview_potentialsubject_changelist') +
            '?q=' + self.kwargs.get('subject_identifier'),
            back_call_url=reverse(
                'call_manager_admin:call_manager_call_changelist') +
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
