# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-11 08:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcpp_interview', '0005_auto_20160811_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpotentialsubject',
            name='pair',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='potentialsubject',
            name='pair',
            field=models.IntegerField(null=True),
        ),
    ]
