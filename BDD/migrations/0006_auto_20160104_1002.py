# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0005_auto_20160104_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typecour',
            name='isExam',
            field=models.BooleanField(default=False),
        ),
    ]
