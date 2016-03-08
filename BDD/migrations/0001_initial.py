# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cour',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 3, 8, 13, 34, 20, 349156, tzinfo=utc))),
                ('semaineMin', models.IntegerField()),
                ('semaineMax', models.IntegerField()),
                ('jour', models.IntegerField(choices=[(0, 'Lundi'), (1, 'Mardi'), (2, 'Mecredi'), (3, 'Jeudi'), (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche')], default=0)),
                ('hmin', models.IntegerField()),
                ('hmax', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Groupe',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('nom', models.CharField(max_length=30)),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 3, 8, 13, 34, 20, 340152, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='horaireProf',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('jdelaSemaine', models.IntegerField(choices=[(0, 'Lundi'), (1, 'Mardi'), (2, 'Mecredi'), (3, 'Jeudi'), (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche')], default=0)),
                ('hminMatin', models.IntegerField()),
                ('hmaxMatin', models.IntegerField()),
                ('hminApresMidi', models.IntegerField()),
                ('hmaxApresMidi', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('nom', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('txt', models.CharField(max_length=100)),
                ('type', models.IntegerField(choices=[(4, 'Statut Inconnu'), (1, 'SALLE'), (2, 'personne'), (3, 'groupe'), (4, 'uv'), (5, 'module'), (6, 'cour'), (7, 'type de cour'), (8, 'notes')], default=4)),
                ('typeG', models.IntegerField(choices=[(0, 'ajout'), (1, 'modifier'), (2, 'suprilmer')], default=0)),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 3, 8, 13, 34, 20, 351157, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('note', models.IntegerField()),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 3, 8, 13, 34, 20, 345156, tzinfo=utc))),
                ('module', models.ForeignKey(to='BDD.Module')),
            ],
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('sexe', models.IntegerField(choices=[(0, 'Sexe Inconnu'), (1, 'Homme'), (2, 'Femme')], default=0)),
                ('adresse', models.CharField(max_length=200, null=True)),
                ('promotion', models.IntegerField(null=True)),
                ('type', models.IntegerField(choices=[(4, 'Statut Inconnu'), (0, 'Prof/Chercheur'), (1, 'Eleve'), (2, 'Administration'), (3, 'Administrateur Du Site')], default=4)),
                ('dateDeNaissance', models.DateField(null=True)),
                ('lieuDeNaissance', models.CharField(max_length=200, null=True)),
                ('numeroDeTel', models.CharField(max_length=40, null=True)),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 3, 8, 13, 34, 20, 335147, tzinfo=utc))),
                ('filter', models.CharField(max_length=200)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Salle',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('nom', models.CharField(max_length=30)),
                ('capacite', models.IntegerField(null=True)),
                ('type', models.IntegerField(choices=[(0, 'Type inconnu'), (1, 'Classe'), (2, 'Labo'), (3, 'Info')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='TypeCour',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('nom', models.CharField(max_length=30)),
                ('isExam', models.BooleanField()),
                ('groupe', models.ManyToManyField(blank=True, to='BDD.Groupe')),
                ('profs', models.ManyToManyField(blank=True, to='BDD.Personne')),
            ],
        ),
        migrations.CreateModel(
            name='UV',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('nom', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='note',
            name='personne',
            field=models.ForeignKey(to='BDD.Personne'),
        ),
        migrations.AddField(
            model_name='note',
            name='prof',
            field=models.ForeignKey(to='BDD.Personne', related_name='ANoter'),
        ),
        migrations.AddField(
            model_name='news',
            name='personne',
            field=models.ManyToManyField(to='BDD.Personne'),
        ),
        migrations.AddField(
            model_name='module',
            name='uv',
            field=models.ForeignKey(to='BDD.UV'),
        ),
        migrations.AddField(
            model_name='horaireprof',
            name='prof',
            field=models.ForeignKey(to='BDD.Personne'),
        ),
        migrations.AddField(
            model_name='groupe',
            name='modules',
            field=models.ManyToManyField(blank=True, to='BDD.Module'),
        ),
        migrations.AddField(
            model_name='groupe',
            name='personnes',
            field=models.ManyToManyField(blank=True, to='BDD.Personne'),
        ),
        migrations.AddField(
            model_name='cour',
            name='salles',
            field=models.ManyToManyField(blank=True, to='BDD.Salle'),
        ),
        migrations.AddField(
            model_name='cour',
            name='typeCour',
            field=models.ForeignKey(to='BDD.TypeCour'),
        ),
    ]
