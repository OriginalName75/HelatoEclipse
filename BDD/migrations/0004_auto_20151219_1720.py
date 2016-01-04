# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0003_groupe_modules'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cour',
            name='jour',
            field=models.IntegerField(choices=[(0, 'Lundi'), (1, 'Mardi'), (2, 'Mecredi'), (3, 'Jeudi'), (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche')], default=0),
        ),
    ]
