# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0007_auto_20160104_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typecour',
            name='nom',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
