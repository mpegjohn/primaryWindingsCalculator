# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-31 15:10
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0014_winding_winding_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='winding',
            name='taps',
            field=models.CharField(default='', max_length=100, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
            preserve_default=False,
        ),
    ]
