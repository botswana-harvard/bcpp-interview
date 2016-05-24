from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Field, Layout, BaseInput, ButtonHolder, Button

from django import forms
from django.db import models
from django.forms import ValidationError
from django.core.urlresolvers import reverse

from edc_call_manager.admin import call_manager_admin
from edc_consent.forms.base_consent_form import BaseConsentForm
from edc_constants.constants import NOT_APPLICABLE
from call_manager.models import LogEntry

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


class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))


class ImportDataForm(forms.Form):

    filename = forms.FilePathField(path='~/')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-import-data-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))


class Cancel(BaseInput):

    input_type = 'submit'

    def __init__(self, *args, **kwargs):
        self.field_classes = 'btn btn-default'
        super(Cancel, self).__init__(*args, **kwargs)


class LogEntryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LogEntryForm, self).__init__(*args, **kwargs)
        fields = self._meta.fields
        if call_manager_admin.is_registered(self._meta.model):
            fields = list(call_manager_admin._registry[self._meta.model].get_fields(None))
            for field_name in [fld for fld in self._meta.model._meta.fields]:
                try:
                    pos = fields.index(field_name)
                    fields.pop(pos)
                    if isinstance(fld, (models.DateTimeField, models.DateField)):
                        fields.insert(pos, self.as_datepicker(field_name, use_time=True))
                    else:
                        fields.insert(pos, field_name)
                except ValueError:
                    pass
        self.helper = FormHelper()
        self.helper.form_id = 'id-call-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse(
            'call_subject', kwargs={'app_label': 'call_manager', 'model_name': 'logentry'})
        self.helper.layout = Layout(
            *fields,
            ButtonHolder(
                Button('cancel-log-entry', 'Cancel'),
                Submit('submit-log-entry', 'Save', css_class="pull-right"),
            ))

    def as_datepicker(self, field, use_time=None):
        if use_time:
            data_date_format = 'yyyy-mm-dd hh:ii'
        else:
            data_date_format = 'yyyy-mm-dd'
        return Field(field, css_class='datetimepicker', attrs={'data-date-format': data_date_format})

    class Meta:
        model = LogEntry
        fields = '__all__'
        widgets = {
            'call_datetime': forms.TextInput(attrs={'class': 'datetimepicker', 'data-date-format': 'yyyy-mm-dd hh:ii'}),
            'appt_date': forms.TextInput(attrs={'class': 'datetimepicker', 'data-date-format': 'yyyy-mm-dd'}),
        }
