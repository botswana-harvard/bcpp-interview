import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.http.response import HttpResponse
from django.shortcuts import render


from bcpp_interview.audio import Audio


class RecordView(TemplateView):
    template_name = 'record.html'

    def __init__(self):
        self.context = {}
        self.filename = None
        self.audio = Audio()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title=settings.PROJECT_TITLE,
            project_name=settings.PROJECT_TITLE,
            is_popup=True,
            name=self.kwargs.get('name'),
            filename='{}.npz'.format(self.kwargs.get('name')),
        )
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RecordView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if request.is_ajax():
            self._user = request.user
            if request.GET.get('action') == 'start_recording':
                self.audio.record(context.get('filename'))
                print(self.audio.filename)
                message = {'message': "started recording", "status": "recording"}
                data = json.dumps([message])
                return HttpResponse(data, content_type='application/json')
            elif request.GET.get('action') == 'stop_recording':
                message = {'message': "stopped recording", "status": self.audio.get_status()}
                self.audio.save()
                data = json.dumps([message])
                return HttpResponse(data, content_type='application/json')
        return render(request, self.template_name, context)
