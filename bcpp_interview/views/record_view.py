import sounddevice as sd

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class RecordView(TemplateView):
    template_name = 'record.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title=settings.PROJECT_TITLE,
            project_name=settings.PROJECT_TITLE,
            is_popup=True,
            name=kwargs.get('name'),
            filename='{}.npz'.format(kwargs.get('name')),
        )
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RecordView, self).dispatch(*args, **kwargs)
