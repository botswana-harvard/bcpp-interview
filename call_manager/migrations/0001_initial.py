# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-06 17:35
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_crypto_fields.fields.encrypted_text_field
import django_crypto_fields.fields.firstname_field
import django_extensions.db.fields
import django_revision.revision_field
import edc_base.model.fields.custom_fields
import edc_base.model.fields.hostname_modification_field
import edc_base.model.fields.userfield
import edc_base.model.fields.uuid_auto_field
import edc_base.model.validators.date


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bcpp_interview', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='mac2-2.local', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(editable=False, help_text='System field. UUID primary key.', primary_key=True, serialize=False)),
                ('subject_identifier', models.CharField(max_length=25)),
                ('label', models.CharField(max_length=25)),
                ('scheduled', models.DateField(default=datetime.date.today)),
                ('repeats', models.BooleanField(default=False)),
                ('last_called', models.DateTimeField(editable=False, help_text='last call datetime updated by call log entry', null=True)),
                ('first_name', django_crypto_fields.fields.firstname_field.FirstnameField(editable=False, help_text=' (Encryption: RSA local)', max_length=71, null=True, verbose_name='First name')),
                ('initials', models.CharField(editable=False, max_length=3, null=True, verbose_name='Initials')),
                ('consent_datetime', models.DateTimeField(help_text='From Subject Consent.', null=True, validators=[edc_base.model.validators.date.datetime_not_before_study_start, edc_base.model.validators.date.datetime_not_future], verbose_name='Consent date and time')),
                ('call_attempts', models.IntegerField(default=0)),
                ('call_outcome', models.TextField(max_length=150, null=True)),
                ('call_status', models.CharField(choices=[('NEW', 'New'), ('open', 'Open'), ('closed', 'Closed')], default='NEW', max_length=15)),
                ('auto_closed', models.BooleanField(default=False, editable=False, help_text='If True call status was changed to CLOSED by EDC.')),
                ('potential_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bcpp_interview.PotentialSubject')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalCall',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='mac2-2.local', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(db_index=True, editable=False, help_text='System field. UUID primary key.')),
                ('subject_identifier', models.CharField(max_length=25)),
                ('label', models.CharField(max_length=25)),
                ('scheduled', models.DateField(default=datetime.date.today)),
                ('repeats', models.BooleanField(default=False)),
                ('last_called', models.DateTimeField(editable=False, help_text='last call datetime updated by call log entry', null=True)),
                ('first_name', django_crypto_fields.fields.firstname_field.FirstnameField(editable=False, help_text=' (Encryption: RSA local)', max_length=71, null=True, verbose_name='First name')),
                ('initials', models.CharField(editable=False, max_length=3, null=True, verbose_name='Initials')),
                ('consent_datetime', models.DateTimeField(help_text='From Subject Consent.', null=True, validators=[edc_base.model.validators.date.datetime_not_before_study_start, edc_base.model.validators.date.datetime_not_future], verbose_name='Consent date and time')),
                ('call_attempts', models.IntegerField(default=0)),
                ('call_outcome', models.TextField(max_length=150, null=True)),
                ('call_status', models.CharField(choices=[('NEW', 'New'), ('open', 'Open'), ('closed', 'Closed')], default='NEW', max_length=15)),
                ('auto_closed', models.BooleanField(default=False, editable=False, help_text='If True call status was changed to CLOSED by EDC.')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('potential_subject', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='bcpp_interview.PotentialSubject')),
            ],
            options={
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical call',
            },
        ),
        migrations.CreateModel(
            name='HistoricalLog',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='mac2-2.local', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(db_index=True, editable=False, help_text='System field. UUID primary key.')),
                ('log_datetime', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('locator_information', django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(help_text='This information has been imported from the previous locator. You may update as required. (Encryption: AES local)', max_length=71, null=True)),
                ('contact_notes', django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=71, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('call', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='call_manager.Call')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical log',
            },
        ),
        migrations.CreateModel(
            name='HistoricalLogEntry',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='mac2-2.local', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(db_index=True, editable=False, help_text='System field. UUID primary key.')),
                ('call_reason', models.CharField(choices=[('schedule_appt', 'Schedule an appointment'), ('reminder', 'Remind participant of scheduled appointment'), ('missed_appt', 'Follow-up with participant on missed appointment')], max_length=25, verbose_name='Reason for this call')),
                ('call_datetime', models.DateTimeField(verbose_name='Date of this call')),
                ('contact_type', models.CharField(choices=[('direct', 'Direct contact with participant'), ('indirect', 'Contact with person other than participant'), ('no_contact', 'No contact made')], help_text='If no contact made. STOP. Save form.', max_length=15)),
                ('survival_status', models.CharField(choices=[('alive', 'Alive'), ('dead', 'Dead'), ('unknown', 'Unknown')], default='alive', max_length=10, null=True, verbose_name='Survival status of the participant')),
                ('time_of_week', models.CharField(blank=True, choices=[('weekdays', 'Weekdays'), ('weekend', 'Weekends')], max_length=25, null=True, verbose_name='Time of week when participant will be available')),
                ('time_of_day', models.CharField(blank=True, choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('evening', 'Evening')], max_length=25, null=True, verbose_name='Time of day when participant will be available')),
                ('appt', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unknown', 'Unknown')], max_length=7, null=True, verbose_name='Is the participant willing to schedule an appointment')),
                ('appt_date', models.DateField(blank=True, help_text='This can only come from the participant.', null=True, validators=[edc_base.model.validators.date.date_is_future], verbose_name='Appointment Date')),
                ('appt_grading', models.CharField(blank=True, choices=[('firm', 'Firm appointment'), ('weak', 'Possible appointment'), ('guess', 'Estimated by RA')], max_length=25, null=True, verbose_name='Is this appointment...')),
                ('appt_location', models.CharField(blank=True, choices=[('home', 'At home'), ('work', 'At work'), ('telephone', 'By telephone'), ('clinic', 'At clinic'), ('OTHER', 'Other location')], max_length=50, null=True, verbose_name='Appointment location')),
                ('appt_location_other', edc_base.model.fields.custom_fields.OtherCharField(blank=True, editable=True, max_length=50, null=True, verbose_name='...if "Other", specify')),
                ('delivered', models.NullBooleanField(default=False, editable=False)),
                ('may_call', models.CharField(blank=True, choices=[('Yes', 'Yes, we may continue to contact the participant.'), ('No', 'No, participant has asked NOT to be contacted again.')], default='Yes', max_length=10, null=True, verbose_name='May we continue to contact the participant?')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical log entry',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='mac2-2.local', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(editable=False, help_text='System field. UUID primary key.', primary_key=True, serialize=False)),
                ('log_datetime', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('locator_information', django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(help_text='This information has been imported from the previous locator. You may update as required. (Encryption: AES local)', max_length=71, null=True)),
                ('contact_notes', django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=71, null=True)),
                ('call', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='call_manager.Call')),
            ],
        ),
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='mac2-2.local', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(editable=False, help_text='System field. UUID primary key.', primary_key=True, serialize=False)),
                ('call_reason', models.CharField(choices=[('schedule_appt', 'Schedule an appointment'), ('reminder', 'Remind participant of scheduled appointment'), ('missed_appt', 'Follow-up with participant on missed appointment')], max_length=25, verbose_name='Reason for this call')),
                ('call_datetime', models.DateTimeField(verbose_name='Date of this call')),
                ('contact_type', models.CharField(choices=[('direct', 'Direct contact with participant'), ('indirect', 'Contact with person other than participant'), ('no_contact', 'No contact made')], help_text='If no contact made. STOP. Save form.', max_length=15)),
                ('survival_status', models.CharField(choices=[('alive', 'Alive'), ('dead', 'Dead'), ('unknown', 'Unknown')], default='alive', max_length=10, null=True, verbose_name='Survival status of the participant')),
                ('time_of_week', models.CharField(blank=True, choices=[('weekdays', 'Weekdays'), ('weekend', 'Weekends')], max_length=25, null=True, verbose_name='Time of week when participant will be available')),
                ('time_of_day', models.CharField(blank=True, choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('evening', 'Evening')], max_length=25, null=True, verbose_name='Time of day when participant will be available')),
                ('appt', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unknown', 'Unknown')], max_length=7, null=True, verbose_name='Is the participant willing to schedule an appointment')),
                ('appt_date', models.DateField(blank=True, help_text='This can only come from the participant.', null=True, validators=[edc_base.model.validators.date.date_is_future], verbose_name='Appointment Date')),
                ('appt_grading', models.CharField(blank=True, choices=[('firm', 'Firm appointment'), ('weak', 'Possible appointment'), ('guess', 'Estimated by RA')], max_length=25, null=True, verbose_name='Is this appointment...')),
                ('appt_location', models.CharField(blank=True, choices=[('home', 'At home'), ('work', 'At work'), ('telephone', 'By telephone'), ('clinic', 'At clinic'), ('OTHER', 'Other location')], max_length=50, null=True, verbose_name='Appointment location')),
                ('appt_location_other', edc_base.model.fields.custom_fields.OtherCharField(blank=True, editable=True, max_length=50, null=True, verbose_name='...if "Other", specify')),
                ('delivered', models.NullBooleanField(default=False, editable=False)),
                ('may_call', models.CharField(blank=True, choices=[('Yes', 'Yes, we may continue to contact the participant.'), ('No', 'No, participant has asked NOT to be contacted again.')], default='Yes', max_length=10, null=True, verbose_name='May we continue to contact the participant?')),
                ('log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='call_manager.Log')),
            ],
        ),
        migrations.AddField(
            model_name='historicallogentry',
            name='log',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='call_manager.Log'),
        ),
    ]
