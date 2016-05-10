# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0004_auto_20160510_0926'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='note',
            new_name='lanote',
        ),
        migrations.AlterField(
            model_name='cour',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 46, 37, 401452, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='groupe',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 46, 37, 375302, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='news',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 46, 37, 406561, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='note',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 46, 37, 390669, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='personne',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 46, 37, 367161, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='typecour',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 46, 37, 393431, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='uv',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 9, 46, 37, 383314, tzinfo=utc)),
        ),
    ]
