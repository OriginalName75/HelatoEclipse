# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0009_auto_20160104_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='champsmodifie',
            name='valchamp',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
