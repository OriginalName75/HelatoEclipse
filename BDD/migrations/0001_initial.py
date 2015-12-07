# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cour',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('uploadDate', models.DateTimeField(default=django.utils.datetime_safe.datetime.now)),
                ('semaineMin', models.IntegerField()),
                ('semaineMax', models.IntegerField()),
                ('jour', models.IntegerField()),
                ('hmin', models.IntegerField()),
                ('hmax', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Groupe',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nom', models.CharField(max_length=30)),
                ('uploadDate', models.DateTimeField(default=django.utils.datetime_safe.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='horaireProf',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('jdelaSemaine', models.IntegerField(choices=[(0, 'Lundi'), (1, 'Mardi'), (2, 'Mecredi'), (3, 'Jeudi'), (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche')])),
                ('hminMatin', models.IntegerField()),
                ('hmaxMatin', models.IntegerField()),
                ('hminApresMidi', models.IntegerField()),
                ('hmaxApresMidi', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nom', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('note', models.IntegerField()),
                ('uploadDate', models.DateTimeField(default=django.utils.datetime_safe.datetime.now)),
                ('module', models.ForeignKey(to='BDD.Module')),
            ],
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('sexe', models.IntegerField(choices=[(0, 'Sexe Inconnu'), (1, 'Homme'), (2, 'Femme')], default=0)),
                ('adresse', models.CharField(max_length=200, null=True)),
                ('promotion', models.IntegerField(null=True)),
                ('type', models.IntegerField(choices=[(4, 'Statut Inconnu'), (0, 'Prof/Chercheur'), (1, 'Eleve'), (2, 'Administration'), (3, 'Administrateur Du Site')], default=4)),
                ('dateDeNaissance', models.DateField(null=True)),
                ('lieuDeNaissance', models.CharField(max_length=200, null=True)),
                ('numeroDeTel', models.CharField(max_length=40, null=True)),
                ('uploadDate', models.DateTimeField(default=django.utils.datetime_safe.datetime.now)),
                ('filter', models.CharField(max_length=200)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Salle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nom', models.CharField(max_length=30)),
                ('capacite', models.IntegerField(null=True)),
                ('type', models.IntegerField(choices=[(0, 'Type inconnu'), (1, 'Classe'), (2, 'Labo'), (3, 'Info')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='TypeCour',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nom', models.CharField(max_length=30)),
                ('isExam', models.BooleanField()),
                ('groupe', models.ManyToManyField(blank=True, to='BDD.Groupe')),
                ('profs', models.ManyToManyField(blank=True, to='BDD.Personne')),
            ],
        ),
        migrations.CreateModel(
            name='UV',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nom', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='note',
            name='personne',
            field=models.ForeignKey(to='BDD.Personne'),
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
