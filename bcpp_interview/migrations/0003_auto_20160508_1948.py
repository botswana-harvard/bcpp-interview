# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-08 19:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcpp_interview', '0002_auto_20160508_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupdiscussionrecording',
            name='sound_filename',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='interviewrecording',
            name='sound_filename',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]