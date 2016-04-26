# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-08 16:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cour',
            name='isvisible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='groupe',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 8, 17, 25, 6, 265055)),
        ),
        migrations.AlterField(
            model_name='news',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 8, 17, 25, 6, 272060)),
        ),
        migrations.AlterField(
            model_name='uv',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 8, 17, 25, 6, 266056)),
        ),
    ]
