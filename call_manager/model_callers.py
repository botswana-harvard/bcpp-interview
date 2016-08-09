from edc_call_manager.model_caller import ModelCaller
from edc_call_manager.decorators import register

from bcpp_interview.models import PotentialSubject, SubjectLocator, SubjectConsent


@register(PotentialSubject, SubjectConsent)
class PotentialSubjectModelCaller(ModelCaller):
    label = 'subjects'
    locator_model = (SubjectLocator, 'potential_subject__subject_identifier')
    subject_model = PotentialSubject
