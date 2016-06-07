# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-07 11:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('call_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicallogentry',
            name='appt_reason_unwilling',
            field=models.CharField(blank=True, choices=[('not_interested', 'Not interested in participating'), ('busy', 'Busy during the suggested times'), ('away', 'Out of town during the suggested times'), ('unavailable', 'Not available during the suggested times'), ('DWTA', 'Prefer not to say why I am unwilling.'), ('OTHER', 'Other reason ...')], max_length=25, null=True, verbose_name='What is the reason the participant is unwilling to schedule an appointment'),
        ),
        migrations.AddField(
            model_name='logentry',
            name='appt_reason_unwilling',
            field=models.CharField(blank=True, choices=[('not_interested', 'Not interested in participating'), ('busy', 'Busy during the suggested times'), ('away', 'Out of town during the suggested times'), ('unavailable', 'Not available during the suggested times'), ('DWTA', 'Prefer not to say why I am unwilling.'), ('OTHER', 'Other reason ...')], max_length=25, null=True, verbose_name='What is the reason the participant is unwilling to schedule an appointment'),
        ),
        migrations.AlterField(
            model_name='historicallogentry',
            name='appt',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=7, null=True, verbose_name='Is the participant willing to schedule an appointment'),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='appt',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=7, null=True, verbose_name='Is the participant willing to schedule an appointment'),
        ),
    ]
