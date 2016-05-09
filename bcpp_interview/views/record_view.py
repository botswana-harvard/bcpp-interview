import os
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.apps import apps as django_apps
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.http.response import HttpResponse
# from django.shortcuts import render, redirect

from bcpp_interview.audio import Audio, RECORDING, READY, AudioError

audio = Audio()


class RecordView(TemplateView):
    template_name = 'record.html'

    def __init__(self):
        self._filename = None
        self.model_instance = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = django_apps.get_model(self.kwargs.get('app_label'), self.kwargs.get('model_name'))
        self.recording_model = django_apps.get_model(
            self.kwargs.get('app_label'),
            self.kwargs.get('model_name') + 'recording')
        self.model_instance = model.objects.get(pk=self.kwargs.get('pk'))
        context.update(
            title=settings.PROJECT_TITLE,
            project_name=settings.PROJECT_TITLE,
            is_popup=True,
            name=self.model_instance.interview_name,
            pk=self.kwargs.get('pk'),
            filename=self.filename,
        )
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RecordView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.is_ajax():
            if request.GET.get('action') == 'start_recording' and audio.get_status() == READY:
                try:
                    audio.record(self.filename, 16000)
                    response_data = {
                        "status": audio.get_status(),
                        "recording_time": audio.duration,
                        "filename": self.filename,
                        "message": "started {}".format(audio.start_datetime.strftime('%H:%M:%S'))}
                except AudioError as e:
                    response_data = {
                        "status": 'Error',
                        "recording_time": '',
                        "filename": self.filename,
                        "message": str(e)}
                return HttpResponse(json.dumps(response_data), content_type='application/json')
            elif request.GET.get('action') == 'stop_recording' and audio.get_status() == RECORDING:
                self.save_recording()
                response_data = {
                    "status": audio.get_status(),
                    "recording_time": audio.duration,
                    "filename": self.filename,
                    "filesize": os.path.getsize(self.filename),
                    "message": ''}
                return HttpResponse(json.dumps(response_data), content_type='application/json')
                # return redirect(self.model_instance)
            elif request.GET.get('action') == 'duration' and audio.get_status() == RECORDING:
                response_data = {
                    "status": audio.get_status(),
                    "recording_time": audio.duration,
                    "filename": self.filename,
                    "message": "started {}".format(audio.start_datetime.strftime('%H:%M:%S'))}
            else:
                response_data = {
                    "status": audio.get_status(),
                    "recording_time": audio.duration,
                    "filename": self.filename,
                    "message": ''}
                try:
                    response_data.update({
                        "message": "started {}".format(audio.start_datetime.strftime('%H:%M:%S'))})
                except AttributeError:
                    pass
                return HttpResponse(json.dumps(response_data), content_type='application/json')
        return self.render_to_response(context)

    @property
    def filename(self):
        if not self._filename:
            temp_filename = str(os.path.join(settings.UPLOAD_FOLDER, self.model_instance.interview_name))
            filename = temp_filename
            n = 1
            while os.path.exists(filename + '.npz'):
                filename = '{}_{}'.format(temp_filename, n)
                n += 1
            self._filename = filename + '.npz'
        return self._filename

    def save_recording(self):
        recording_attr = '_'.join(self.model_instance._meta.verbose_name.split(' ')).lower()
        audio.save(compress=True, reset=False)
        recording_options = {
            recording_attr: self.model_instance,
            'start_datetime': audio.start_datetime,
            'stop_datetime': audio.stop_datetime,
            'recording_time': audio.duration,
            'sound_file': self.filename,
            'sound_filename': self.filename,
            'sound_filesize': os.path.getsize(self.filename)}
        self.model_instance.interviewed = True
        self.model_instance.save()
        self.recording_model.objects.create(
            **recording_options)
        audio.reset()
