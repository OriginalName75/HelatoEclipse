# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0002_auto_20151205_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupe',
            name='modules',
            field=models.ManyToManyField(blank=True, to='BDD.Module'),
        ),
    ]
