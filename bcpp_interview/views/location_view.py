from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse

from edc_map.views import MapImageView

from ..models import SubjectLocation


class LocationView(MapImageView):

    template_name = 'location.html'
    item_model = SubjectLocation
    item_model_field = 'subject_identifier'
    app_label = 'bcpp_map'
    filename_field = 'subject_identifier'

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
        return context
