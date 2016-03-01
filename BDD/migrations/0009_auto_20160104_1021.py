# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0008_auto_20160104_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typecour',
            name='nom',
            field=models.CharField(max_length=30),
        ),
    ]
