# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Annee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('annee', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Cour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nom', models.CharField(max_length=30)),
                ('isExam', models.BooleanField()),
                ('uploadDate', models.DateTimeField(default=django.utils.datetime_safe.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Groupe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nom', models.CharField(max_length=30)),
                ('uploadDate', models.DateTimeField(default=django.utils.datetime_safe.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nom', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Moi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nom', models.CharField(max_length=30)),
                ('nbMoi', models.IntegerField()),
                ('annee', models.ForeignKey(to='BDD.Annee')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('note', models.IntegerField()),
                ('uploadDate', models.DateTimeField(default=django.utils.datetime_safe.datetime.now)),
                ('module', models.ForeignKey(to='BDD.Module')),
            ],
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nom', models.CharField(max_length=30)),
                ('capacite', models.IntegerField(null=True)),
                ('type', models.IntegerField(choices=[(0, 'Type inconnu'), (1, 'Classe'), (2, 'Labo'), (3, 'Info')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Semaine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('semaine', models.IntegerField()),
                ('moi', models.ForeignKey(to='BDD.Moi')),
            ],
        ),
        migrations.CreateModel(
            name='UV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
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
            model_name='groupe',
            name='personnes',
            field=models.ManyToManyField(to='BDD.Personne', blank=True),
        ),
        migrations.AddField(
            model_name='cour',
            name='groupe',
            field=models.ManyToManyField(to='BDD.Groupe', blank=True),
        ),
        migrations.AddField(
            model_name='cour',
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
            name='semaine',
            field=models.ForeignKey(to='BDD.Semaine', null=True),
        ),
    ]
