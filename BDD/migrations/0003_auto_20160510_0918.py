# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0002_auto_20160510_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cour',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 18, 33, 491076, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='groupe',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 18, 33, 467786, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='news',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 18, 33, 495917, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='note',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 18, 33, 481270, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='personne',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 18, 33, 462511, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='typecour',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 18, 33, 484092, tzinfo=utc)),
        ),
    ]
