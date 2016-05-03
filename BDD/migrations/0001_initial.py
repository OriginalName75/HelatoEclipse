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
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('txt', models.CharField(max_length=100)),
                ('type', models.IntegerField(default=4, choices=[(4, b'Statut Inconnu'), (1, b'SALLE'), (2, b'personne'), (3, b'groupe'), (4, b'uv'), (5, b'module'), (6, b'cour'), (7, b'type de cour'), (8, b'notes')])),
                ('typeG', models.IntegerField(default=0, choices=[(0, b'ajout'), (1, b'modifier'), (2, b'suprilmer')])),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 3, 29, 10, 26, 34, 46010, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='PaternModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cour',
            fields=[
                ('paternmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='BDD.PaternModel')),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 3, 29, 10, 26, 34, 41972, tzinfo=utc))),
                ('semaineMin', models.IntegerField()),
                ('semaineMax', models.IntegerField()),
                ('jour', models.IntegerField(default=0, choices=[(0, b'Lundi'), (1, b'Mardi'), (2, b'Mecredi'), (3, b'Jeudi'), (4, b'Vendredi'), (5, b'Samedi'), (6, b'Dimanche')])),
                ('hmin', models.IntegerField()),
                ('hmax', models.IntegerField()),
            ],
            bases=('BDD.paternmodel',),
        ),
        migrations.CreateModel(
            name='Groupe',
            fields=[
                ('paternmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='BDD.PaternModel')),
                ('nom', models.CharField(max_length=30)),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 3, 29, 10, 26, 34, 24954, tzinfo=utc))),
            ],
            bases=('BDD.paternmodel',),
        ),
        migrations.CreateModel(
            name='horaireProf',
            fields=[
                ('paternmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='BDD.PaternModel')),
                ('jdelaSemaine', models.IntegerField(default=0, choices=[(0, b'Lundi'), (1, b'Mardi'), (2, b'Mecredi'), (3, b'Jeudi'), (4, b'Vendredi'), (5, b'Samedi'), (6, b'Dimanche')])),
                ('hminMatin', models.IntegerField()),
                ('hmaxMatin', models.IntegerField()),
                ('hminApresMidi', models.IntegerField()),
                ('hmaxApresMidi', models.IntegerField()),
            ],
            bases=('BDD.paternmodel',),
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('paternmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='BDD.PaternModel')),
                ('nom', models.CharField(max_length=30)),
            ],
            bases=('BDD.paternmodel',),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('paternmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='BDD.PaternModel')),
                ('note', models.IntegerField(default=0, null=True, blank=True)),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 3, 29, 10, 26, 34, 35029, tzinfo=utc))),
                ('module', models.ForeignKey(to='BDD.Module')),
            ],
            bases=('BDD.paternmodel',),
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('paternmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='BDD.PaternModel')),
                ('sexe', models.IntegerField(default=0, choices=[(0, b'Sexe Inconnu'), (1, b'Homme'), (2, b'Femme')])),
                ('adresse', models.CharField(max_length=200, null=True)),
                ('promotion', models.IntegerField(null=True)),
                ('type', models.IntegerField(default=4, choices=[(4, b'Statut Inconnu'), (0, b'Prof/Chercheur'), (1, b'Eleve'), (2, b'Administration'), (3, b'Administrateur Du Site')])),
                ('dateDeNaissance', models.DateField(null=True)),
                ('lieuDeNaissance', models.CharField(max_length=200, null=True)),
                ('numeroDeTel', models.CharField(max_length=40, null=True)),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 3, 29, 10, 26, 34, 20358, tzinfo=utc))),
                ('filter', models.CharField(max_length=200)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            bases=('BDD.paternmodel',),
        ),
        migrations.CreateModel(
            name='Salle',
            fields=[
                ('paternmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='BDD.PaternModel')),
                ('nom', models.CharField(max_length=30)),
                ('capacite', models.IntegerField(null=True)),
                ('type', models.IntegerField(default=0, choices=[(0, b'Type inconnu'), (1, b'Classe'), (2, b'Labo'), (3, b'Info')])),
            ],
            bases=('BDD.paternmodel',),
        ),
        migrations.CreateModel(
            name='TypeCour',
            fields=[
                ('paternmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='BDD.PaternModel')),
                ('nom', models.CharField(max_length=30)),
                ('isExam', models.BooleanField()),
                ('groupe', models.ManyToManyField(to='BDD.Groupe', blank=True)),
                ('profs', models.ManyToManyField(to='BDD.Personne', blank=True)),
            ],
            bases=('BDD.paternmodel',),
        ),
        migrations.CreateModel(
            name='UV',
            fields=[
                ('paternmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='BDD.PaternModel')),
                ('nom', models.CharField(max_length=30)),
            ],
            bases=('BDD.paternmodel',),
        ),
        migrations.AddField(
            model_name='note',
            name='personne',
            field=models.ForeignKey(to='BDD.Personne'),
        ),
        migrations.AddField(
            model_name='note',
            name='prof',
            field=models.ForeignKey(related_name='ANoter', to='BDD.Personne'),
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
