import json
import pytz
from datetime import date, datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from edc_constants.constants import CLOSED, NO, YES
from edc_sync.models.outgoing_transaction import OutgoingTransaction

from call_manager.models import Call

from ..models import PotentialSubject, InterviewRecording, GroupDiscussionRecording

tz = pytz.timezone(settings.TIME_ZONE)


class StatisticsView(TemplateView):
    template_name = 'home.html'

    def __init__(self):
        self._response_data = {}
        self.columns = [
            'consented',
            'consented_today',
            'contacted_retry',
            'contacted_today',
            'idi_not_verified',
            'fgd_not_verified',
            'fgd_complete',
            'fgd_complete_today',
            'idi_complete',
            'idi_complete_today',
            'not_consented',
            'not_contacted',
            'not_interviewed',
            'pending_transactions',
            'potential_subjects']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title=settings.PROJECT_TITLE,
            project_name=settings.PROJECT_TITLE,
        )
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StatisticsView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.is_ajax():
            self.response_data.update(self.potential_subject_data)
            self.response_data.update(self.transaction_data)
            self.response_data.update(self.contact_data)
            return HttpResponse(json.dumps(self.response_data), content_type='application/json')
        return self.render_to_response(context)

    @property
    def contact_data(self):
        response_data = {}
        calls = Call.objects.filter(call_attempts__gte=1)
        if calls:
            response_data.update(contacted_retry=calls.exclude(call_status=CLOSED).count())
            calls.filter(**self.modified_option)
            if calls:
                response_data.update(contacted_today=calls.count())
        return self.verified_response_data(response_data)

    @property
    def transaction_data(self):
        response_data = {}
        tx = OutgoingTransaction.objects.filter(is_consumed_server=False)
        if tx:
            response_data.update(pending_transactions=tx.count())
        return self.verified_response_data(response_data)

    @property
    def potential_subject_data(self):
        response_data = {}
        potential_subjects = PotentialSubject.objects.all()
        if potential_subjects:
            response_data.update({
                'potential_subjects': potential_subjects.count(),
                'not_contacted': potential_subjects.filter(contacted=False).count(),
                'not_consented': potential_subjects.filter(consented=False).count(),
                'not_interviewed': potential_subjects.filter(interviewed=False).count(),
                'consented': potential_subjects.filter(consented=True).count(),
                'idi_not_verified': InterviewRecording.objects.filter(verified=NO).count(),
                'fgd_not_verified': GroupDiscussionRecording.objects.filter(verified=NO).count(),
                'idi_complete': potential_subjects.filter(idi=True).count(),
                'fgd_complete': potential_subjects.filter(fgd=True).count(),
            })
            potential_subjects = potential_subjects.filter(**self.modified_option)
            response_data.update({
                'consented_today': potential_subjects.filter(consented=True).count(),
                'idi_complete_today': InterviewRecording.objects.filter(
                    verified=YES, **self.modified_option).count(),
                'fgd_complete_today': GroupDiscussionRecording.objects.filter(
                    verified=YES, **self.modified_option).count(),
            })
        return self.verified_response_data(response_data)

    @property
    def modified_option(self):
        d = date.today()
        return {'modified__gte': tz.localize(datetime(d.year, d.month, d.day, 0, 0, 0))}

    def verified_response_data(self, response_data):
        diff = set(response_data.keys()).difference(set(self.response_data.keys()))
        if diff:
            raise KeyError('Invalid key or keys in response data dictionary. Got {}'.format(diff))
        return response_data

    @property
    def response_data(self):
        if not self._response_data:
            self._response_data = dict(zip(self.columns, len(self.columns) * [0]))
        return self._response_data
