# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0003_auto_20151214_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupe',
            name='isvisible',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='module',
            name='isvisible',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='note',
            name='isvisible',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personne',
            name='isvisible',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='salle',
            name='isvisible',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='typecour',
            name='isvisible',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='uv',
            name='isvisible',
            field=models.BooleanField(default=False),
        ),
    ]
