# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0004_auto_20151214_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typecour',
            name='nom',
            field=models.CharField(null=True, max_length=30),
        ),
    ]
