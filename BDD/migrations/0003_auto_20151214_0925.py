# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('BDD', '0002_auto_20151205_2228'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChampsModifie',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nomchamp', models.CharField(max_length=50)),
                ('valchamp', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Modification',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('datemodif', models.DateTimeField(default=django.utils.datetime_safe.datetime.now)),
                ('typetable', models.CharField(null=True, max_length=200)),
                ('typemod', models.IntegerField(choices=[(0, 'statut Inconnu'), (1, 'Supprimé'), (2, 'Ajouté'), (3, 'Modifié')], default=0)),
            ],
        ),
        migrations.AddField(
            model_name='champsmodifie',
            name='champs',
            field=models.ForeignKey(to='BDD.Modification'),
        ),
    ]
