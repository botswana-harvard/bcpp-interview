# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-08 19:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcpp_interview', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupdiscussionrecording',
            name='recording_time',
            field=models.FloatField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='interviewrecording',
            name='recording_time',
            field=models.FloatField(editable=False, null=True),
        ),
    ]