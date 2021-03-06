# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-05 12:41
from __future__ import unicode_literals

from django.db import migrations
import django_crypto_fields.fields.encrypted_text_field
import edc_base.model.fields.uuid_auto_field


class Migration(migrations.Migration):

    dependencies = [
        ('bcpp_interview', '0002_auto_20160630_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='focusgroup',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='focusgroupitem',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='groupdiscussion',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='groupdiscussionlabel',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='groupdiscussionrecording',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='historicalfocusgroup',
            name='history_id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='historicalfocusgroup',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, db_index=True, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalfocusgroupitem',
            name='history_id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='historicalfocusgroupitem',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, db_index=True, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalgroupdiscussion',
            name='history_id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='historicalgroupdiscussion',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, db_index=True, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalgroupdiscussionlabel',
            name='history_id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='historicalgroupdiscussionlabel',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, db_index=True, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalgroupdiscussionrecording',
            name='history_id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='historicalgroupdiscussionrecording',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, db_index=True, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalinterview',
            name='history_id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='historicalinterview',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, db_index=True, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalinterviewrecording',
            name='history_id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='historicalinterviewrecording',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, db_index=True, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalnurseconsent',
            name='history_id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='historicalnurseconsent',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, db_index=True, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalpotentialsubject',
            name='history_id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='historicalpotentialsubject',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, db_index=True, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalsubjectconsent',
            name='history_id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='historicalsubjectconsent',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, db_index=True, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='historicalsubjectlocator',
            name='contact_physical_address',
            field=django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=71, null=True, verbose_name='Full physical address '),
        ),
        migrations.AlterField(
            model_name='historicalsubjectlocator',
            name='history_id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='historicalsubjectlocator',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, db_index=True, editable=False, help_text='System auto field. UUID primary key.'),
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
            name='history_id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='historicalsubjectloss',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, db_index=True, editable=False, help_text='System auto field. UUID primary key.'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='interviewrecording',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='nurseconsent',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='potentialsubject',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='rawdata',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='subjectconsent',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='subjectlocation',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='subjectlocator',
            name='contact_physical_address',
            field=django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(blank=True, help_text=' (Encryption: AES local)', max_length=71, null=True, verbose_name='Full physical address '),
        ),
        migrations.AlterField(
            model_name='subjectlocator',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
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
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='survey',
            name='id',
            field=edc_base.model.fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False),
        ),
    ]
