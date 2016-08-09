from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from edc_base.views import EdcBaseViewMixin

from django.apps import apps as django_apps


class HomeView(EdcBaseViewMixin, TemplateView):
    template_name = 'bcpp_interview/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            site_header=admin.site.site_header,
        )
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)
