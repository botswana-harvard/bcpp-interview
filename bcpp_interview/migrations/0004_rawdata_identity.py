# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-02 15:59
from __future__ import unicode_literals

from django.db import migrations
import django_crypto_fields.fields.identity_field


class Migration(migrations.Migration):

    dependencies = [
        ('bcpp_interview', '0003_auto_20160602_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawdata',
            name='identity',
            field=django_crypto_fields.fields.identity_field.IdentityField(help_text=' (Encryption: RSA local)', max_length=71, null=True),
        ),
    ]
