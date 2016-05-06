from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class TranslateView(TemplateView):
    template_name = 'translate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title=settings.PROJECT_TITLE,
            project_name=settings.PROJECT_TITLE
        )
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TranslateView, self).dispatch(*args, **kwargs)