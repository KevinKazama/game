# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0035_message_crypt'),
    ]

    operations = [
        migrations.CreateModel(
            name='staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prenom', models.CharField(max_length=20)),
                ('nom', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='table_equipement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type_equip', models.CharField(max_length=20)),
                ('durabilite', models.IntegerField(default=50)),
                ('ptsservice', models.IntegerField(default=0)),
                ('ptsretour', models.IntegerField(default=0)),
                ('ptsconcentration', models.IntegerField(default=0)),
                ('ptsendurance', models.IntegerField(default=0)),
                ('prix', models.IntegerField(default=0)),
                ('proprio', models.ForeignKey(to='jeutennis.table_joueurs')),
            ],
        ),
    ]
