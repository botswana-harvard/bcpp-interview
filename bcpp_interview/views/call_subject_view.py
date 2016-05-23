from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse

from ..forms import LogEntryForm
from call_manager.models import Log, LogEntry
from bcpp_interview.models import PotentialSubject
from edc_base.utils.age import formatted_age


class CallSubjectView(FormView):

    form_class = LogEntryForm
    template_name = 'call_subject.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        log = Log.objects.get(pk=self.kwargs.get('pk'))
        subject_identifier = log.call.subject_identifier
        call_status = log.call.get_call_status_display()
        subject = PotentialSubject.objects.get(subject_identifier=subject_identifier)
        context.update(
            title=settings.PROJECT_TITLE,
            project_name=settings.PROJECT_TITLE,
            log_entry_form=LogEntryForm(),
            contact_information=log.locator_information,
            contact_history=LogEntry.objects.filter(log=log).order_by('-call_datetime'),
            subject_identifier=subject_identifier,
            name='{} {}'.format(subject.first_name or '', subject.last_name or ''),
            gender=subject.gender,
            age=formatted_age(subject.dob),
            call_status=(call_status or log.call.call_status),
            pk=self.kwargs.get('pk'),
        )
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CallSubjectView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('call_manager_admin:call_manager_call_changelist')

    def form_valid(self, form):
        return self.form_invalid(form)
