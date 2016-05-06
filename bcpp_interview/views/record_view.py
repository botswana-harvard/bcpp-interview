import sounddevice as sd
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


class RecordView(TemplateView):
    template_name = 'record.html'

    def __init__(self):
        self.context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title=settings.PROJECT_TITLE,
            project_name=settings.PROJECT_TITLE,
            is_popup=True,
            name=kwargs.get('name'),
        )
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RecordView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.context = self.get_context_data()
        if request.is_ajax():
            self._user = request.user
            if request.GET.get('action') == 'start_recording':
                message = {'message': "started recording", "status": "recording"}
                data = json.dumps([message])
                return HttpResponse(data, content_type='application/json')
            elif request.GET.get('action') == 'stop_recording':
                message = {'message': "stopped recording", "status": "stopped_recording"}
                data = json.dumps([message])
                return HttpResponse(data, content_type='application/json')
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))
