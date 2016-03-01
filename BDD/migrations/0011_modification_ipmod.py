# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0010_auto_20160104_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='modification',
            name='ipmod',
            field=models.IntegerField(null=True, max_length=200),
        ),
    ]
