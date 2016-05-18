# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-18 19:51
from __future__ import unicode_literals

import bcpp_interview.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_crypto_fields.fields.encrypted_char_field
import django_crypto_fields.fields.encrypted_text_field
import django_extensions.db.fields
import django_revision.revision_field
import edc_base.model.fields.hostname_modification_field
import edc_base.model.fields.userfield
import edc_base.model.fields.uuid_auto_field
import edc_base.model.validators.phone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bcpp_interview', '0002_historicalgroupdiscussionrecording_historicalinterviewrecording'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalGroupDiscussion',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='mac2-2.local', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(db_index=True, editable=False, help_text='System field. UUID primary key.')),
                ('report_datetime', models.DateTimeField(editable=False, null=True)),
                ('reference', models.CharField(db_index=True, default=bcpp_interview.models.interview_identifier, max_length=7)),
                ('interview_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('location', models.TextField(max_length=100, verbose_name='Where is this interview being conducted?')),
                ('interviewed', models.BooleanField(default=False, editable=False)),
                ('comment', django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=250, null=True, verbose_name='Additional comment that may assist in analysis of this discussion')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('focus_group', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='bcpp_interview.FocusGroup')),
                ('group_discussion_label', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='bcpp_interview.GroupDiscussionLabel')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'history_date',
                'verbose_name': 'historical group discussion',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='HistoricalGroupDiscussionLabel',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='mac2-2.local', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(db_index=True, editable=False, help_text='System field. UUID primary key.')),
                ('discussion_label', models.CharField(db_index=True, max_length=50)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'history_date',
                'verbose_name': 'historical group discussion label',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='HistoricalInterview',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='mac2-2.local', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(db_index=True, editable=False, help_text='System field. UUID primary key.')),
                ('report_datetime', models.DateTimeField(editable=False, null=True)),
                ('reference', models.CharField(db_index=True, default=bcpp_interview.models.interview_identifier, max_length=7)),
                ('interview_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('location', models.TextField(max_length=100, verbose_name='Where is this interview being conducted?')),
                ('interviewed', models.BooleanField(default=False, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('potential_subject', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='bcpp_interview.PotentialSubject')),
            ],
            options={
                'get_latest_by': 'history_date',
                'verbose_name': 'historical In-depth Interview',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='HistoricalSubjectLocator',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='mac2-2.local', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(db_index=True, editable=False, help_text='System field. UUID primary key.')),
                ('date_signed', models.DateField(default=datetime.date.today, verbose_name='Date Locator Form signed ')),
                ('mail_address', django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=500, null=True, verbose_name='Mailing address ')),
                ('home_visit_permission', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=25, verbose_name='Has the participant given his/her permission for study staff to make home visits for follow-up purposes during the study?')),
                ('physical_address', django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=500, null=True, verbose_name='Physical address with detailed description')),
                ('may_follow_up', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=25, verbose_name='Has the participant given his/her permission for study staff to call her for follow-up purposes during the study?')),
                ('may_sms_follow_up', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=25, null=True, verbose_name='Has the participant given his/her permission for study staff to SMS her for follow-up purposes during the study?')),
                ('subject_cell', django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(blank=True, help_text=' (Encryption: RSA local)', max_length=8, null=True, validators=[edc_base.model.validators.phone.CellNumber], verbose_name='Cell number')),
                ('subject_cell_alt', django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(blank=True, help_text=' (Encryption: RSA local)', max_length=8, null=True, validators=[edc_base.model.validators.phone.CellNumber], verbose_name='Cell number (alternate)')),
                ('subject_phone', django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(blank=True, help_text=' (Encryption: RSA local)', max_length=8, null=True, validators=[edc_base.model.validators.phone.TelephoneNumber], verbose_name='Telephone')),
                ('subject_phone_alt', django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(blank=True, help_text=' (Encryption: RSA local)', max_length=8, null=True, validators=[edc_base.model.validators.phone.TelephoneNumber], verbose_name='Telephone (alternate)')),
                ('may_call_work', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('Doesnt_work', 'Doesnt Work')], max_length=25, verbose_name='Has the participant given his/her permission for study staff to contact her at work for follow up purposes during the study?')),
                ('subject_work_place', django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=500, null=True, verbose_name='Name and location of work place')),
                ('subject_work_phone', django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(blank=True, help_text=' (Encryption: RSA local)', max_length=8, null=True, verbose_name='Work contact number ')),
                ('may_contact_someone', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='For example a partner, spouse, family member, neighbour ...', max_length=25, verbose_name='Has the participant given his/her permission for study staff to contact anyone else for follow-up purposes during the study?')),
                ('contact_name', django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(blank=True, help_text=' (Encryption: RSA local)', max_length=35, null=True, verbose_name='Full names of the contact person')),
                ('contact_rel', django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(blank=True, help_text=' (Encryption: RSA local)', max_length=35, null=True, verbose_name='Relationship to participant')),
                ('contact_physical_address', django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=500, null=True, verbose_name='Full physical address ')),
                ('contact_cell', django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(blank=True, help_text=' (Encryption: RSA local)', max_length=8, null=True, validators=[edc_base.model.validators.phone.CellNumber], verbose_name='Cell number')),
                ('contact_phone', django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(blank=True, help_text=' (Encryption: RSA local)', max_length=8, null=True, validators=[edc_base.model.validators.phone.TelephoneNumber], verbose_name='Telephone number')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('potential_subject', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='bcpp_interview.PotentialSubject')),
            ],
            options={
                'get_latest_by': 'history_date',
                'verbose_name': 'historical subject locator',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
    ]
