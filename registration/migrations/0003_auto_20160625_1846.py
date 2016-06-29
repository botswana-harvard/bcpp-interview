# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-25 16:46
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20160625_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalregisteredsubject',
            name='history_id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]