# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0011_modification_ipmod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modification',
            name='ipmod',
            field=models.IntegerField(null=True),
        ),
    ]
