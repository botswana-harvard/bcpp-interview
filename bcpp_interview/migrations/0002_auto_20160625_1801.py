# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-25 16:01
from __future__ import unicode_literals

import bcpp_interview.models
from django.db import migrations, models
import django_crypto_fields.fields.encrypted_text_field
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bcpp_interview', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='focusgroup',
            name='id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='focusgroup',
            name='reference',
            field=models.CharField(default=bcpp_interview.models.group_identifier, max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='focusgroupitem',
            name='id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='groupdiscussion',
            name='id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='groupdiscussionlabel',
            name='id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='groupdiscussionrecording',
            name='id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='historicalfocusgroup',
            name='id',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalfocusgroup',
            name='reference',
            field=models.CharField(db_index=True, default=bcpp_interview.models.group_identifier, max_length=15),
        ),
        migrations.AlterField(
            model_name='historicalfocusgroupitem',
            name='id',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalgroupdiscussion',
            name='id',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalgroupdiscussionlabel',
            name='id',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalgroupdiscussionrecording',
            name='id',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalinterview',
            name='id',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalinterviewrecording',
            name='id',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalnurseconsent',
            name='id',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalpotentialsubject',
            name='id',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalsubjectconsent',
            name='id',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalsubjectlocator',
            name='contact_physical_address',
            field=django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=71, null=True, verbose_name='Full physical address '),
        ),
        migrations.AlterField(
            model_name='historicalsubjectlocator',
            name='id',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalsubjectlocator',
            name='mail_address',
            field=django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=71, null=True, verbose_name='Mailing address '),
        ),
        migrations.AlterField(
            model_name='historicalsubjectlocator',
            name='physical_address',
            field=django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=71, null=True, verbose_name='Physical address with detailed description'),
        ),
        migrations.AlterField(
            model_name='historicalsubjectlocator',
            name='subject_work_place',
            field=django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=71, null=True, verbose_name='Name and location of work place'),
        ),
        migrations.AlterField(
            model_name='historicalsubjectloss',
            name='id',
            field=models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='interviewrecording',
            name='id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='nurseconsent',
            name='id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='potentialsubject',
            name='id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='rawdata',
            name='id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='subjectconsent',
            name='id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='subjectlocation',
            name='id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='subjectlocator',
            name='contact_physical_address',
            field=django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=71, null=True, verbose_name='Full physical address '),
        ),
        migrations.AlterField(
            model_name='subjectlocator',
            name='id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='subjectlocator',
            name='mail_address',
            field=django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=71, null=True, verbose_name='Mailing address '),
        ),
        migrations.AlterField(
            model_name='subjectlocator',
            name='physical_address',
            field=django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=71, null=True, verbose_name='Physical address with detailed description'),
        ),
        migrations.AlterField(
            model_name='subjectlocator',
            name='subject_work_place',
            field=django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=71, null=True, verbose_name='Name and location of work place'),
        ),
        migrations.AlterField(
            model_name='subjectloss',
            name='id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='survey',
            name='id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
    ]
