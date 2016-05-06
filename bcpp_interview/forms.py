from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from edc_consent.forms.base_consent_form import BaseConsentForm

from .models import SubjectConsent


class SubjectConsentForm(BaseConsentForm):

    class Meta:
        model = SubjectConsent
        fields = '__all__'


class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
