from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.urlresolvers import reverse
from call_manager.models import Call


class CallForm(forms.ModelForm):

    protocol = forms.CharField(
        label="BHP Protocol Number ")

    def __init__(self, *args, **kwargs):
        super(CallForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-protocol-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('home')
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Call
        fields = '__all__'
