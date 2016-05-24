# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
from django.utils.timezone import utc
import datetime
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChampsModifie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nomchamp', models.CharField(max_length=50)),
                ('valchamp', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 5, 10, 13, 45, 33, 293997, tzinfo=utc))),
                ('semaineMin', models.IntegerField()),
                ('semaineMax', models.IntegerField()),
                ('jour', models.IntegerField(default=0, choices=[(0, 'Lundi'), (1, 'Mardi'), (2, 'Mecredi'), (3, 'Jeudi'), (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche')])),
                ('hmin', models.IntegerField()),
                ('hmax', models.IntegerField()),
                ('isvisible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Groupe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nom', models.CharField(max_length=30)),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 5, 10, 13, 45, 33, 277509, tzinfo=utc))),
                ('isvisible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='horaireProf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('jdelaSemaine', models.IntegerField(default=0, choices=[(0, 'Lundi'), (1, 'Mardi'), (2, 'Mecredi'), (3, 'Jeudi'), (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche')])),
                ('hminMatin', models.IntegerField()),
                ('hmaxMatin', models.IntegerField()),
                ('hminApresMidi', models.IntegerField()),
                ('hmaxApresMidi', models.IntegerField()),
                ('isvisible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Modification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('datemodif', models.DateTimeField(default=django.utils.datetime_safe.datetime.now)),
                ('typetable', models.CharField(max_length=200, null=True)),
                ('typemod', models.IntegerField(default=0, choices=[(0, 'Ajout'), (1, 'Modifier'), (2, 'Supprimer'), (0, 'mod statut inconnu')])),
                ('ipmod', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nom', models.CharField(max_length=30)),
                ('isvisible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('txt', models.CharField(max_length=100)),
                ('type', models.IntegerField(default=4, choices=[(4, 'Statut Inconnu'), (1, 'SALLE'), (2, 'personne'), (3, 'groupe'), (4, 'uv'), (5, 'module'), (6, 'cour'), (7, 'type de cour'), (8, 'notes')])),
                ('typeG', models.IntegerField(default=0, choices=[(0, 'ajout'), (1, 'modifier'), (2, 'suprilmer')])),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 5, 10, 13, 45, 33, 297113, tzinfo=utc))),
                ('isvisible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('lanote', models.IntegerField(default=0, null=True, blank=True)),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 5, 10, 13, 45, 33, 285554, tzinfo=utc))),
                ('isvisible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('sexe', models.IntegerField(default=0, choices=[(0, 'Sexe Inconnu'), (1, 'Homme'), (2, 'Femme')])),
                ('adresse', models.CharField(max_length=200, null=True)),
                ('promotion', models.IntegerField(null=True)),
                ('type', models.IntegerField(default=4, choices=[(4, 'Statut Inconnu'), (0, 'Prof/Chercheur'), (1, 'Eleve'), (2, 'Administration'), (3, 'Administrateur Du Site')])),
                ('dateDeNaissance', models.DateField(null=True)),
                ('lieuDeNaissance', models.CharField(max_length=200, null=True)),
                ('numeroDeTel', models.CharField(max_length=40, null=True)),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 5, 10, 13, 45, 33, 274365, tzinfo=utc))),
                ('filter', models.CharField(max_length=200)),
                ('isvisible', models.BooleanField(default=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Salle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nom', models.CharField(max_length=30)),
                ('capacite', models.IntegerField(null=True)),
                ('type', models.IntegerField(default=0, choices=[(0, 'Type inconnu'), (1, 'Classe'), (2, 'Labo'), (3, 'Info')])),
                ('isvisible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='TypeCour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nom', models.CharField(max_length=30)),
                ('isExam', models.BooleanField()),
                ('isvisible', models.BooleanField(default=True)),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 5, 10, 13, 45, 33, 287335, tzinfo=utc))),
                ('groupe', models.ManyToManyField(to='BDD.Groupe', blank=True)),
                ('profs', models.ManyToManyField(to='BDD.Personne', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nom', models.CharField(max_length=30)),
                ('isvisible', models.BooleanField(default=True)),
                ('uploadDate', models.DateTimeField(default=datetime.datetime(2016, 5, 10, 13, 45, 33, 281483, tzinfo=utc))),
            ],
        ),
        migrations.AddField(
            model_name='note',
            name='personnenote',
            field=models.ForeignKey(to='BDD.Personne'),
        ),
        migrations.AddField(
            model_name='note',
            name='prof',
            field=models.ForeignKey(to='BDD.Personne', related_name='ANoter'),
        ),
        migrations.AddField(
            model_name='note',
            name='themodule',
            field=models.ForeignKey(to='BDD.Module'),
        ),
        migrations.AddField(
            model_name='news',
            name='personne',
            field=models.ManyToManyField(to='BDD.Personne'),
        ),
        migrations.AddField(
            model_name='module',
            name='theuv',
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
        migrations.AddField(
            model_name='champsmodifie',
            name='champs',
            field=models.ForeignKey(to='BDD.Modification'),
        ),
    ]
