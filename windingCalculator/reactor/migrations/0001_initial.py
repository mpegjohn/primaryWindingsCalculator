# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lamination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lam_size', models.CharField(max_length=20)),
                ('measure_A', models.FloatField()),
                ('measure_B', models.FloatField()),
                ('measure_C', models.FloatField()),
                ('measure_D', models.FloatField()),
                ('measure_E', models.FloatField()),
                ('measure_F', models.FloatField()),
                ('measure_G', models.FloatField()),
                ('path_length', models.FloatField()),
                ('window_area', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Winding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('turns', models.IntegerField()),
                ('layers', models.IntegerField()),
                ('turns_per_layer', models.IntegerField()),
                ('voltage', models.FloatField()),
                ('current', models.FloatField()),
                ('mean_length_turns', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Wire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('diameter', models.FloatField()),
                ('grade_1_dia_max', models.FloatField()),
                ('grade_2_dia_max', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='winding',
            name='wire',
            field=models.ForeignKey(to='reactor.Wire'),
            preserve_default=True,
        ),
    ]
