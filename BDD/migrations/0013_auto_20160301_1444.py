# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0012_auto_20160202_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='uploadDate',
            field=models.DateTimeField(default=django.utils.datetime_safe.datetime.now),
        ),
        migrations.AddField(
            model_name='salle',
            name='uploadDate',
            field=models.DateTimeField(default=django.utils.datetime_safe.datetime.now),
        ),
        migrations.AddField(
            model_name='typecour',
            name='uploadDate',
            field=models.DateTimeField(default=django.utils.datetime_safe.datetime.now),
        ),
        migrations.AddField(
            model_name='uv',
            name='uploadDate',
            field=models.DateTimeField(default=django.utils.datetime_safe.datetime.now),
        ),
    ]
