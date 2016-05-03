from django.contrib import admin


from .models import SubjectConsent
from .forms import SubjectConsentForm
from edc_consent.admin import BaseConsentModelAdmin


@admin.register(SubjectConsent)
class SubjectConsentAdmin(BaseConsentModelAdmin):

    form = SubjectConsentForm
    date_hierarchy = 'consent_datetime'

    list_display = [
        'subject_identifier', 'is_verified', 'is_verified_datetime', 'first_name',
        'initials', 'gender', 'dob', 'consent_datetime', 'created', 'modified',
        'user_created', 'user_modified']
    search_fields = ['id', 'subject_identifier', 'first_name', 'last_name', 'identity']

    # actions = [flag_as_verified_against_paper, unflag_as_verified_against_paper]

    list_filter = [
        'gender',
        'is_verified',
        'is_verified_datetime',
        'language',
        'study_site',
        'is_literate',
        'consent_datetime',
        'created',
        'modified',
        'user_created',
        'user_modified',
        'hostname_created']
    fields = [
        'subject_identifier',
        'first_name',
        'last_name',
        'initials',
        'language',
        'is_literate',
        'witness_name',
        'consent_datetime',
        'study_site',
        'gender',
        'dob',
        'guardian_name',
        'is_dob_estimated',
        'identity',
        'identity_type',
        'confirm_identity',
        'is_incarcerated',
        'comment',
        'consent_reviewed',
        'study_questions',
        'assessment_score',
        'consent_copy']

    radio_fields = {
        "language": admin.VERTICAL,
        "gender": admin.VERTICAL,
        # "study_site": admin.VERTICAL,
        "is_dob_estimated": admin.VERTICAL,
        "identity_type": admin.VERTICAL,
        "is_incarcerated": admin.VERTICAL,
        "consent_reviewed": admin.VERTICAL,
        "study_questions": admin.VERTICAL,
        "assessment_score": admin.VERTICAL,
        "consent_copy": admin.VERTICAL,
        "is_literate": admin.VERTICAL}

    # override to disallow subject to be changed
    def get_readonly_fields(self, request, obj=None):
        super(BaseConsentModelAdmin, self).get_readonly_fields(request, obj)
        if obj:  # In edit mode
            return (
                'subject_identifier',
                'subject_identifier_as_pk',
                'study_site',
                'consent_datetime',) + self.readonly_fields
        else:
            return ('subject_identifier', 'subject_identifier_as_pk',) + self.readonly_fields
