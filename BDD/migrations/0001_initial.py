# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.datetime_safe
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cour',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('uploadDate', models.DateTimeField(default=django.utils.datetime_safe.datetime.now)),
                ('semaineMin', models.IntegerField()),
                ('semaineMax', models.IntegerField()),
                ('jour', models.IntegerField(default=0, choices=[(0, 'Lundi'), (1, 'Mardi'), (2, 'Mecredi'), (3, 'Jeudi'), (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche')])),
                ('hmin', models.IntegerField()),
                ('hmax', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Groupe',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('nom', models.CharField(max_length=30)),
                ('uploadDate', models.DateTimeField(default=django.utils.datetime_safe.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='horaireProf',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('jdelaSemaine', models.IntegerField(default=0, choices=[(0, 'Lundi'), (1, 'Mardi'), (2, 'Mecredi'), (3, 'Jeudi'), (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche')])),
                ('hminMatin', models.IntegerField()),
                ('hmaxMatin', models.IntegerField()),
                ('hminApresMidi', models.IntegerField()),
                ('hmaxApresMidi', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('nom', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('note', models.IntegerField()),
                ('uploadDate', models.DateTimeField(default=django.utils.datetime_safe.datetime.now)),
                ('module', models.ForeignKey(to='BDD.Module')),
            ],
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('sexe', models.IntegerField(default=0, choices=[(0, 'Sexe Inconnu'), (1, 'Homme'), (2, 'Femme')])),
                ('adresse', models.CharField(null=True, max_length=200)),
                ('promotion', models.IntegerField(null=True)),
                ('type', models.IntegerField(default=4, choices=[(4, 'Statut Inconnu'), (0, 'Prof/Chercheur'), (1, 'Eleve'), (2, 'Administration'), (3, 'Administrateur Du Site')])),
                ('dateDeNaissance', models.DateField(null=True)),
                ('lieuDeNaissance', models.CharField(null=True, max_length=200)),
                ('numeroDeTel', models.CharField(null=True, max_length=40)),
                ('uploadDate', models.DateTimeField(default=django.utils.datetime_safe.datetime.now)),
                ('filter', models.CharField(max_length=200)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Salle',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('nom', models.CharField(max_length=30)),
                ('capacite', models.IntegerField(null=True)),
                ('type', models.IntegerField(default=0, choices=[(0, 'Type inconnu'), (1, 'Classe'), (2, 'Labo'), (3, 'Info')])),
            ],
        ),
        migrations.CreateModel(
            name='TypeCour',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('nom', models.CharField(max_length=30)),
                ('isExam', models.BooleanField()),
                ('groupe', models.ManyToManyField(to='BDD.Groupe', blank=True)),
                ('profs', models.ManyToManyField(to='BDD.Personne', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UV',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
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
            field=models.ManyToManyField(to='BDD.Module', blank=True),
        ),
        migrations.AddField(
            model_name='groupe',
            name='personnes',
            field=models.ManyToManyField(to='BDD.Personne', blank=True),
        ),
        migrations.AddField(
            model_name='cour',
            name='salles',
            field=models.ManyToManyField(to='BDD.Salle', blank=True),
        ),
        migrations.AddField(
            model_name='cour',
            name='typeCour',
            field=models.ForeignKey(to='BDD.TypeCour'),
        ),
    ]
