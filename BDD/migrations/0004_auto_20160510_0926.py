# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0003_auto_20160510_0918'),
    ]

    operations = [
        migrations.AddField(
            model_name='uv',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 26, 53, 8091, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cour',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 26, 53, 28502, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='groupe',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 26, 52, 999694, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='news',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 26, 53, 33807, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='note',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 26, 53, 18316, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='personne',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 26, 52, 994432, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='typecour',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 26, 53, 21404, tzinfo=utc)),
        ),
    ]
