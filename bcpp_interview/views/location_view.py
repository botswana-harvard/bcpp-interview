from edc_map.views import MapImageView

from ..models import SubjectLocation


class LocationView(MapImageView):

    template_name = 'location.html'
    item_model = SubjectLocation
    item_model_field = 'subject_identifier'
    app_label = 'bcpp_map'
