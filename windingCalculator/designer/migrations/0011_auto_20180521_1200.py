# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-21 12:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0010_remove_bobbin_has_terminals'),
    ]

    operations = [
        migrations.CreateModel(
            name='general_properties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('value', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='steel',
            name='gapped_permeability',
            field=models.FloatField(default=1000.0),
        ),
        migrations.AlterField(
            model_name='steel',
            name='grade',
            field=models.CharField(default='M6', max_length=100),
        ),
        migrations.AlterField(
            model_name='steel',
            name='name',
            field=models.CharField(default='M6 x 0.35', max_length=100),
        ),
        migrations.AlterField(
            model_name='steel',
            name='thickness',
            field=models.FloatField(default=0.35),
        ),
    ]
