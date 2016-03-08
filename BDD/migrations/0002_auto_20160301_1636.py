# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cour',
            name='annee',
        ),
        migrations.AlterField(
            model_name='groupe',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 1, 16, 36, 45, 255368)),
        ),
        migrations.AlterField(
            model_name='news',
            name='type',
            field=models.IntegerField(choices=[(4, 'Statut Inconnu'), (1, 'SALLE'), (2, 'personne'), (3, 'groupe'), (4, 'uv'), (5, 'module'), (6, 'cour'), (7, 'type de cour'), (8, 'notes')], default=4),
        ),
        migrations.AlterField(
            model_name='news',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 1, 16, 36, 45, 286377)),
        ),
        migrations.AlterField(
            model_name='note',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 1, 16, 36, 45, 271374)),
        ),
        migrations.AlterField(
            model_name='personne',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 1, 16, 36, 45, 249365)),
        ),
    ]
