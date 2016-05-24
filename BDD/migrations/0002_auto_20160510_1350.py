# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 13, 50, 58, 218939, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cour',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 13, 50, 58, 230494, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='groupe',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 13, 50, 58, 213451, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='news',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 13, 50, 58, 233532, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='note',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 13, 50, 58, 221605, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='personne',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 13, 50, 58, 210199, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='typecour',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 13, 50, 58, 223551, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='uv',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 13, 50, 58, 217495, tzinfo=utc)),
        ),
    ]
