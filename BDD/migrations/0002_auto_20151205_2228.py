# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horaireprof',
            name='jdelaSemaine',
            field=models.IntegerField(default=0, choices=[(0, 'Lundi'), (1, 'Mardi'), (2, 'Mecredi'), (3, 'Jeudi'), (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche')]),
        ),
    ]
