from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import ValidationError


from edc_consent.forms.base_consent_form import BaseConsentForm
from edc_constants.constants import NOT_APPLICABLE

from .models import SubjectConsent, PotentialSubject, INITIATED


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


class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
