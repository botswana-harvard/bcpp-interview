from edc_consent.forms.base_consent_form import BaseConsentForm

from .models import SubjectConsent


class SubjectConsentForm(BaseConsentForm):

    class Meta:
        model = SubjectConsent
        fields = '__all__'
