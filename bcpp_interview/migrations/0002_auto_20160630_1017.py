# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-30 08:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bcpp_interview', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='interview',
            unique_together=set([('reference', 'potential_subject')]),
        ),
    ]
