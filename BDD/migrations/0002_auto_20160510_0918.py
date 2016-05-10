# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='typecour',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 18, 19, 283744, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cour',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 18, 19, 297702, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='groupe',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 18, 19, 259425, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='news',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 18, 19, 303258, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='note',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 18, 19, 280986, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='personne',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 18, 19, 252980, tzinfo=utc)),
        ),
    ]
