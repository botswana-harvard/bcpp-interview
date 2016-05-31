from django import forms
from django.forms import ValidationError

from edc_consent.forms.base_consent_form import BaseConsentForm
from edc_constants.constants import NOT_APPLICABLE

from .models import NurseConsent, SubjectConsent, PotentialSubject, INITIATED


class PotentialSubjectForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(PotentialSubjectForm, self).clean()
        if cleaned_data.get('category') == INITIATED and cleaned_data.get('sub_category') == NOT_APPLICABLE:
            forms.ValidationError('Please specify a sub-category for \'ART initiated\' potential subjects.')
        elif cleaned_data.get('category') != INITIATED and cleaned_data.get('sub_category') != NOT_APPLICABLE:
            forms.ValidationError('Sub-category {} is only applicable to \'ART initiated\' potential subjects.')
        return cleaned_data

    class Meta:
        model = PotentialSubject
        fields = '__all__'


class SubjectConsentForm(BaseConsentForm):

    def clean(self):
        cleaned_data = super(SubjectConsentForm, self).clean()
        SubjectConsent.fetch_potential_subject(cleaned_data.get('identity'), ValidationError)
        return cleaned_data

    class Meta:
        model = SubjectConsent
        exclude = ['study_site']


class NurseConsentForm(BaseConsentForm):

    class Meta:
        model = NurseConsent
        exclude = ['study_site', 'guardian_name']
