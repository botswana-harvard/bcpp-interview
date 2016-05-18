from django.core import serializers
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from bcpp_interview.models import SubjectConsent
from django.http.response import HttpResponse


class ConsentView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title=settings.PROJECT_TITLE,
            project_name=settings.PROJECT_TITLE,
            site_header=admin.site.site_header,
            pill='consent',
        )
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ConsentView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.is_ajax():
            response_data = SubjectConsent.objects.all()
            return HttpResponse(
                serializers.serialize("json", response_data),
                content_type='application/json')
        return self.render_to_response(context)
