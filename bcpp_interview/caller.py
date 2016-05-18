from edc_call_manager.model_caller import ModelCaller
from edc_call_manager.decorators import register

from .models import PotentialSubject, SubjectConsent, SubjectLocator


@register(PotentialSubject)
class PotentialSubjectModelCaller(ModelCaller):
    label = 'subjects'
    consent_model = SubjectConsent
    locator_model = SubjectLocator
