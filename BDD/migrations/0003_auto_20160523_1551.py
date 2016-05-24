# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0002_auto_20160510_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='sens',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='cour',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 23, 13, 51, 21, 928804, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='groupe',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 23, 13, 51, 21, 921715, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='module',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 23, 13, 51, 21, 925303, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='news',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 23, 13, 51, 21, 930805, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='note',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 23, 13, 51, 21, 926303, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='personne',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 23, 13, 51, 21, 920214, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='typecour',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 23, 13, 51, 21, 927303, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='uv',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 23, 13, 51, 21, 923216, tzinfo=utc)),
        ),
    ]
