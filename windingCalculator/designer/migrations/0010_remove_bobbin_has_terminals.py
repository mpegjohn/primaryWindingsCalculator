# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-14 12:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0009_auto_20180514_0749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bobbin',
            name='has_terminals',
        ),
    ]
