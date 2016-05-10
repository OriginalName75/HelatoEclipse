# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.datetime_safe
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChampsModifie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('nomchamp', models.CharField(max_length=50)),
                ('valchamp', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Modification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('datemodif', models.DateTimeField(default=django.utils.datetime_safe.datetime.now)),
                ('typetable', models.CharField(max_length=200, null=True)),
                ('typemod', models.IntegerField(default=0, choices=[(0, 'Ajout'), (1, 'Modifier'), (2, 'Supprimer'), (0, 'mod statut inconnu')])),
                ('ipmod', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('txt', models.CharField(max_length=100)),
                ('type', models.IntegerField(default=4, choices=[(4, 'Statut Inconnu'), (1, 'SALLE'), (2, 'personne'), (3, 'groupe'), (4, 'uv'), (5, 'module'), (6, 'cour'), (7, 'type de cour'), (8, 'notes')])),
                ('typeG', models.IntegerField(default=0, choices=[(0, 'ajout'), (1, 'modifier'), (2, 'suprilmer')])),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 5, 10, 11, 53, 30, 950068, tzinfo=utc))),
                ('isvisible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaternModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cour',
            fields=[
                ('paternmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='BDD.PaternModel', serialize=False, primary_key=True)),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 5, 10, 11, 53, 30, 946809, tzinfo=utc))),
                ('semaineMin', models.IntegerField()),
                ('semaineMax', models.IntegerField()),
                ('jour', models.IntegerField(default=0, choices=[(0, 'Lundi'), (1, 'Mardi'), (2, 'Mecredi'), (3, 'Jeudi'), (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche')])),
                ('hmin', models.IntegerField()),
                ('hmax', models.IntegerField()),
                ('isvisible', models.BooleanField(default=True)),
            ],
            bases=('BDD.paternmodel',),
        ),
        migrations.CreateModel(
            name='Groupe',
            fields=[
                ('paternmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='BDD.PaternModel', serialize=False, primary_key=True)),
                ('nom', models.CharField(max_length=30)),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 5, 10, 11, 53, 30, 929639, tzinfo=utc))),
                ('isvisible', models.BooleanField(default=True)),
            ],
            bases=('BDD.paternmodel',),
        ),
        migrations.CreateModel(
            name='horaireProf',
            fields=[
                ('paternmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='BDD.PaternModel', serialize=False, primary_key=True)),
                ('jdelaSemaine', models.IntegerField(default=0, choices=[(0, 'Lundi'), (1, 'Mardi'), (2, 'Mecredi'), (3, 'Jeudi'), (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche')])),
                ('hminMatin', models.IntegerField()),
                ('hmaxMatin', models.IntegerField()),
                ('hminApresMidi', models.IntegerField()),
                ('hmaxApresMidi', models.IntegerField()),
                ('isvisible', models.BooleanField(default=True)),
            ],
            bases=('BDD.paternmodel',),
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('paternmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='BDD.PaternModel', serialize=False, primary_key=True)),
                ('nom', models.CharField(max_length=30)),
                ('isvisible', models.BooleanField(default=True)),
            ],
            bases=('BDD.paternmodel',),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('paternmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='BDD.PaternModel', serialize=False, primary_key=True)),
                ('lanote', models.IntegerField(default=0, null=True, blank=True)),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 5, 10, 11, 53, 30, 938156, tzinfo=utc))),
                ('isvisible', models.BooleanField(default=True)),
                ('module', models.ForeignKey(to='BDD.Module')),
            ],
            bases=('BDD.paternmodel',),
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('paternmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='BDD.PaternModel', serialize=False, primary_key=True)),
                ('sexe', models.IntegerField(default=0, choices=[(0, 'Sexe Inconnu'), (1, 'Homme'), (2, 'Femme')])),
                ('adresse', models.CharField(max_length=200, null=True)),
                ('promotion', models.IntegerField(null=True)),
                ('type', models.IntegerField(default=4, choices=[(4, 'Statut Inconnu'), (0, 'Prof/Chercheur'), (1, 'Eleve'), (2, 'Administration'), (3, 'Administrateur Du Site')])),
                ('dateDeNaissance', models.DateField(null=True)),
                ('lieuDeNaissance', models.CharField(max_length=200, null=True)),
                ('numeroDeTel', models.CharField(max_length=40, null=True)),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 5, 10, 11, 53, 30, 925949, tzinfo=utc))),
                ('filter', models.CharField(max_length=200)),
                ('isvisible', models.BooleanField(default=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            bases=('BDD.paternmodel',),
        ),
        migrations.CreateModel(
            name='Salle',
            fields=[
                ('paternmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='BDD.PaternModel', serialize=False, primary_key=True)),
                ('nom', models.CharField(max_length=30)),
                ('capacite', models.IntegerField(null=True)),
                ('type', models.IntegerField(default=0, choices=[(0, 'Type inconnu'), (1, 'Classe'), (2, 'Labo'), (3, 'Info')])),
                ('isvisible', models.BooleanField(default=True)),
            ],
            bases=('BDD.paternmodel',),
        ),
        migrations.CreateModel(
            name='TypeCour',
            fields=[
                ('paternmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='BDD.PaternModel', serialize=False, primary_key=True)),
                ('nom', models.CharField(max_length=30)),
                ('isExam', models.BooleanField()),
                ('isvisible', models.BooleanField(default=True)),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 5, 10, 11, 53, 30, 939939, tzinfo=utc))),
                ('groupe', models.ManyToManyField(to='BDD.Groupe', blank=True)),
                ('profs', models.ManyToManyField(to='BDD.Personne', blank=True)),
            ],
            bases=('BDD.paternmodel',),
        ),
        migrations.CreateModel(
            name='UV',
            fields=[
                ('paternmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='BDD.PaternModel', serialize=False, primary_key=True)),
                ('nom', models.CharField(max_length=30)),
                ('isvisible', models.BooleanField(default=True)),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 5, 10, 11, 53, 30, 933925, tzinfo=utc))),
            ],
            bases=('BDD.paternmodel',),
        ),
        migrations.AddField(
            model_name='champsmodifie',
            name='champs',
            field=models.ForeignKey(to='BDD.Modification'),
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
