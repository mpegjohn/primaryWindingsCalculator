# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-31 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0012_auto_20180526_0649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inductor',
            name='winding',
        ),
        migrations.AddField(
            model_name='inductor',
            name='windings',
            field=models.ManyToManyField(to='designer.Winding'),
        ),
    ]
