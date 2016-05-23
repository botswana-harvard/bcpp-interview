from edc_call_manager.model_caller import ModelCaller
from edc_call_manager.decorators import register

from bcpp_interview.models import PotentialSubject, SubjectLocator, SubjectConsent
from call_manager.models import Call, Log, LogEntry


@register(PotentialSubject)
class PotentialSubjectModelCaller(ModelCaller):
    label = 'subjects'
    locator_model = (SubjectLocator, 'potential_subject__subject_identifier')
    call_model = (Call, 'potential_subject')
    log_model = Log
    log_entry_model = LogEntry
    unscheduling_model = SubjectConsent
