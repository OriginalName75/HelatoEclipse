# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0013_auto_20160301_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupe',
            name='isvisible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='isvisible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='isvisible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='personne',
            name='isvisible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='salle',
            name='isvisible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='typecour',
            name='isvisible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='uv',
            name='isvisible',
            field=models.BooleanField(default=True),
        ),
    ]
