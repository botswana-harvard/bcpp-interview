# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-24 05:54
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django_crypto_fields.fields.encrypted_char_field
import django_crypto_fields.fields.encrypted_text_field
import django_crypto_fields.fields.firstname_field
import django_crypto_fields.fields.identity_field
import django_crypto_fields.fields.lastname_field
import django_crypto_fields.mixins
import django_extensions.db.fields
import django_revision.revision_field
import edc_base.model.fields.custom_fields
import edc_base.model.fields.hostname_modification_field
import edc_base.model.fields.userfield
import edc_base.model.fields.uuid_auto_field
import edc_base.model.validators.date
import edc_consent.models.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bcpp_interview', '0006_auto_20160522_1646'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalNurseConsent',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='mac2-2.local', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(db_index=True, editable=False, help_text='System field. UUID primary key.')),
                ('citizen', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3, verbose_name='Are you a Botswana citizen? ')),
                ('legal_marriage', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', help_text="If 'NO' participant will not be enrolled.", max_length=3, null=True, verbose_name='If not a citizen, are you legally married to a Botswana Citizen?')),
                ('marriage_certificate', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', help_text="If 'NO' participant will not be enrolled.", max_length=3, null=True, verbose_name='[Interviewer] Has the participant produced the marriage certificate, as proof? ')),
                ('marriage_certificate_no', models.CharField(blank=True, help_text='e.g. 000/YYYY', max_length=9, null=True, verbose_name='What is the marriage certificate number?')),
                ('first_name', django_crypto_fields.fields.firstname_field.FirstnameField(help_text=' (Encryption: RSA local)', max_length=71, null=True)),
                ('last_name', django_crypto_fields.fields.lastname_field.LastnameField(help_text=' (Encryption: RSA local)', max_length=71, null=True, verbose_name='Last name')),
                ('initials', django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(help_text=' (Encryption: RSA local)', max_length=71, null=True, validators=[django.core.validators.RegexValidator(message='Ensure initials consist of letters only in upper case, no spaces.', regex='^[A-Z]{2,3}$')])),
                ('dob', models.DateField(help_text='Format is YYYY-MM-DD', null=True, verbose_name='Date of birth')),
                ('is_dob_estimated', edc_base.model.fields.custom_fields.IsDateEstimatedField(choices=[('-', 'No'), ('D', 'Yes, estimated the Day'), ('MD', 'Yes, estimated Month and Day'), ('YMD', 'Yes, estimated Year, Month and Day')], help_text='If the exact date is not known, please indicate which part of the date is estimated.', max_length=25, null=True, verbose_name='Is date of birth estimated?')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Undetermined')], max_length=1, null=True, verbose_name='Gender')),
                ('guardian_name', django_crypto_fields.fields.lastname_field.LastnameField(blank=True, help_text="Required only if subject is a minor. Format is 'LASTNAME, FIRSTNAME'. All uppercase separated by a comma then followe by a space. (Encryption: RSA local)", max_length=71, null=True, validators=[edc_consent.models.validators.FullNameValidator()], verbose_name="Guardian's Last and first name (minors only)")),
                ('subject_type', models.CharField(max_length=25)),
                ('consent_reviewed', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If no, INELIGIBLE', max_length=3, null=True, validators=[edc_consent.models.validators.eligible_if_yes], verbose_name='I have reviewed the consent with the client')),
                ('study_questions', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If no, INELIGIBLE', max_length=3, null=True, validators=[edc_consent.models.validators.eligible_if_yes], verbose_name='I have answered all questions the client had about the study')),
                ('assessment_score', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If no, INELIGIBLE', max_length=3, null=True, validators=[edc_consent.models.validators.eligible_if_yes], verbose_name='I have asked the client questions about this study and they have demonstrated understanding')),
                ('consent_signature', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If no, INELIGIBLE', max_length=3, null=True, validators=[edc_consent.models.validators.eligible_if_yes], verbose_name='The client has signed the consent form?')),
                ('consent_copy', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('Declined', 'Yes, but subject declined copy')], help_text='If declined, return copy to the clinic with the consent', max_length=20, null=True, validators=[edc_consent.models.validators.eligible_if_yes_or_declined], verbose_name='I have provided the client with a copy of their signed informed consent')),
                ('is_incarcerated', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='-', help_text="( if 'Yes' STOP patient cannot be consented )", max_length=3, null=True, validators=[edc_consent.models.validators.eligible_if_no], verbose_name='Is the participant under involuntary incarceration?')),
                ('is_literate', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default=None, help_text="( if 'No' provide witness's name on this form and signature on the paper document.)", max_length=3, verbose_name='Is the participant LITERATE?')),
                ('witness_name', django_crypto_fields.fields.lastname_field.LastnameField(blank=True, help_text="Required only if subject is illiterate. Format is 'LASTNAME, FIRSTNAME'. All uppercase separated by a comma. (Encryption: RSA local)", max_length=71, null=True, validators=[edc_consent.models.validators.FullNameValidator()], verbose_name="Witness's Last and first name (illiterates only)")),
                ('language', models.CharField(choices=[('tn', 'Setswana'), ('en', 'English')], default='not specified', help_text='The language used for the edc_consent process will also be used during data collection.', max_length=25, verbose_name='Language of edc_consent')),
                ('is_verified', models.BooleanField(default=False, editable=False)),
                ('is_verified_datetime', models.DateTimeField(editable=False, null=True)),
                ('verified_by', models.CharField(editable=False, max_length=25, null=True)),
                ('subject_identifier', models.CharField(blank=True, max_length=50, verbose_name='Subject Identifier')),
                ('subject_identifier_as_pk', models.CharField(default=None, editable=False, max_length=50, verbose_name='Subject Identifier as pk')),
                ('subject_identifier_aka', models.CharField(editable=False, help_text='track a previously allocated identifier.', max_length=50, null=True, verbose_name='Subject Identifier a.k.a')),
                ('consent_datetime', models.DateTimeField(validators=[edc_base.model.validators.date.datetime_not_before_study_start, edc_base.model.validators.date.datetime_not_future], verbose_name='Consent date and time')),
                ('version', models.CharField(default='?', editable=False, help_text="See 'Consent Type' for consent versions by period.", max_length=10, verbose_name='Consent version')),
                ('study_site', models.CharField(max_length=15, null=True)),
                ('sid', models.CharField(blank=True, help_text='Used for randomization against a prepared rando-list.', max_length=15, null=True, verbose_name='SID')),
                ('comment', django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=250, null=True, verbose_name='Comment')),
                ('dm_comment', models.CharField(editable=False, help_text='see also edc.data manager.', max_length=150, null=True, verbose_name='Data Management comment')),
                ('identity', django_crypto_fields.fields.identity_field.IdentityField(help_text="Use Omang, Passport number, driver's license number or Omang receipt number (Encryption: RSA local)", max_length=71, verbose_name='Identity number (OMANG, etc)')),
                ('identity_type', edc_base.model.fields.custom_fields.IdentityTypeField(choices=[('OMANG', 'Omang'), ('DRIVERS', "Driver's License"), ('PASSPORT', 'Passport'), ('OMANG_RCPT', 'Omang Receipt'), ('OTHER', 'Other')], max_length=15, verbose_name='What type of identity number is this?')),
                ('confirm_identity', django_crypto_fields.fields.identity_field.IdentityField(help_text='Retype the identity number from the identity card (Encryption: RSA local)', max_length=71, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical nurse consent',
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='NurseConsent',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='mac2-2.local', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(editable=False, help_text='System field. UUID primary key.', primary_key=True, serialize=False)),
                ('citizen', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3, verbose_name='Are you a Botswana citizen? ')),
                ('legal_marriage', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', help_text="If 'NO' participant will not be enrolled.", max_length=3, null=True, verbose_name='If not a citizen, are you legally married to a Botswana Citizen?')),
                ('marriage_certificate', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], default='N/A', help_text="If 'NO' participant will not be enrolled.", max_length=3, null=True, verbose_name='[Interviewer] Has the participant produced the marriage certificate, as proof? ')),
                ('marriage_certificate_no', models.CharField(blank=True, help_text='e.g. 000/YYYY', max_length=9, null=True, verbose_name='What is the marriage certificate number?')),
                ('first_name', django_crypto_fields.fields.firstname_field.FirstnameField(help_text=' (Encryption: RSA local)', max_length=71, null=True)),
                ('last_name', django_crypto_fields.fields.lastname_field.LastnameField(help_text=' (Encryption: RSA local)', max_length=71, null=True, verbose_name='Last name')),
                ('initials', django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(help_text=' (Encryption: RSA local)', max_length=71, null=True, validators=[django.core.validators.RegexValidator(message='Ensure initials consist of letters only in upper case, no spaces.', regex='^[A-Z]{2,3}$')])),
                ('dob', models.DateField(help_text='Format is YYYY-MM-DD', null=True, verbose_name='Date of birth')),
                ('is_dob_estimated', edc_base.model.fields.custom_fields.IsDateEstimatedField(choices=[('-', 'No'), ('D', 'Yes, estimated the Day'), ('MD', 'Yes, estimated Month and Day'), ('YMD', 'Yes, estimated Year, Month and Day')], help_text='If the exact date is not known, please indicate which part of the date is estimated.', max_length=25, null=True, verbose_name='Is date of birth estimated?')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Undetermined')], max_length=1, null=True, verbose_name='Gender')),
                ('guardian_name', django_crypto_fields.fields.lastname_field.LastnameField(blank=True, help_text="Required only if subject is a minor. Format is 'LASTNAME, FIRSTNAME'. All uppercase separated by a comma then followe by a space. (Encryption: RSA local)", max_length=71, null=True, validators=[edc_consent.models.validators.FullNameValidator()], verbose_name="Guardian's Last and first name (minors only)")),
                ('subject_type', models.CharField(max_length=25)),
                ('consent_reviewed', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If no, INELIGIBLE', max_length=3, null=True, validators=[edc_consent.models.validators.eligible_if_yes], verbose_name='I have reviewed the consent with the client')),
                ('study_questions', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If no, INELIGIBLE', max_length=3, null=True, validators=[edc_consent.models.validators.eligible_if_yes], verbose_name='I have answered all questions the client had about the study')),
                ('assessment_score', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If no, INELIGIBLE', max_length=3, null=True, validators=[edc_consent.models.validators.eligible_if_yes], verbose_name='I have asked the client questions about this study and they have demonstrated understanding')),
                ('consent_signature', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='If no, INELIGIBLE', max_length=3, null=True, validators=[edc_consent.models.validators.eligible_if_yes], verbose_name='The client has signed the consent form?')),
                ('consent_copy', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('Declined', 'Yes, but subject declined copy')], help_text='If declined, return copy to the clinic with the consent', max_length=20, null=True, validators=[edc_consent.models.validators.eligible_if_yes_or_declined], verbose_name='I have provided the client with a copy of their signed informed consent')),
                ('is_incarcerated', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='-', help_text="( if 'Yes' STOP patient cannot be consented )", max_length=3, null=True, validators=[edc_consent.models.validators.eligible_if_no], verbose_name='Is the participant under involuntary incarceration?')),
                ('is_literate', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default=None, help_text="( if 'No' provide witness's name on this form and signature on the paper document.)", max_length=3, verbose_name='Is the participant LITERATE?')),
                ('witness_name', django_crypto_fields.fields.lastname_field.LastnameField(blank=True, help_text="Required only if subject is illiterate. Format is 'LASTNAME, FIRSTNAME'. All uppercase separated by a comma. (Encryption: RSA local)", max_length=71, null=True, validators=[edc_consent.models.validators.FullNameValidator()], verbose_name="Witness's Last and first name (illiterates only)")),
                ('language', models.CharField(choices=[('tn', 'Setswana'), ('en', 'English')], default='not specified', help_text='The language used for the edc_consent process will also be used during data collection.', max_length=25, verbose_name='Language of edc_consent')),
                ('is_verified', models.BooleanField(default=False, editable=False)),
                ('is_verified_datetime', models.DateTimeField(editable=False, null=True)),
                ('verified_by', models.CharField(editable=False, max_length=25, null=True)),
                ('subject_identifier', models.CharField(blank=True, max_length=50, verbose_name='Subject Identifier')),
                ('subject_identifier_as_pk', models.CharField(default=None, editable=False, max_length=50, verbose_name='Subject Identifier as pk')),
                ('subject_identifier_aka', models.CharField(editable=False, help_text='track a previously allocated identifier.', max_length=50, null=True, verbose_name='Subject Identifier a.k.a')),
                ('consent_datetime', models.DateTimeField(validators=[edc_base.model.validators.date.datetime_not_before_study_start, edc_base.model.validators.date.datetime_not_future], verbose_name='Consent date and time')),
                ('version', models.CharField(default='?', editable=False, help_text="See 'Consent Type' for consent versions by period.", max_length=10, verbose_name='Consent version')),
                ('study_site', models.CharField(max_length=15, null=True)),
                ('sid', models.CharField(blank=True, help_text='Used for randomization against a prepared rando-list.', max_length=15, null=True, verbose_name='SID')),
                ('comment', django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=250, null=True, verbose_name='Comment')),
                ('dm_comment', models.CharField(editable=False, help_text='see also edc.data manager.', max_length=150, null=True, verbose_name='Data Management comment')),
                ('identity', django_crypto_fields.fields.identity_field.IdentityField(help_text="Use Omang, Passport number, driver's license number or Omang receipt number (Encryption: RSA local)", max_length=71, verbose_name='Identity number (OMANG, etc)')),
                ('identity_type', edc_base.model.fields.custom_fields.IdentityTypeField(choices=[('OMANG', 'Omang'), ('DRIVERS', "Driver's License"), ('PASSPORT', 'Passport'), ('OMANG_RCPT', 'Omang Receipt'), ('OTHER', 'Other')], max_length=15, verbose_name='What type of identity number is this?')),
                ('confirm_identity', django_crypto_fields.fields.identity_field.IdentityField(help_text='Retype the identity number from the identity card (Encryption: RSA local)', max_length=71, null=True)),
            ],
            options={
                'get_latest_by': 'consent_datetime',
                'ordering': ('created',),
            },
            bases=(django_crypto_fields.mixins.CryptoMixin, models.Model),
            managers=[
                ('consent', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='nurseconsent',
            unique_together=set([('first_name', 'dob', 'initials', 'version')]),
        ),
    ]
