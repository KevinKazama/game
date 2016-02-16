# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='table_joueurs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prenom', models.CharField(max_length=20)),
                ('nom', models.CharField(max_length=20)),
                ('date_naissance', models.DateField(verbose_name=b'naissance')),
                ('service', models.DecimalField(default=b'0.00', max_digits=2, decimal_places=2)),
                ('retour', models.DecimalField(default=b'0.00', max_digits=2, decimal_places=2)),
                ('concentration', models.DecimalField(default=b'0.00', max_digits=2, decimal_places=2)),
                ('endurance', models.DecimalField(default=b'0.00', max_digits=2, decimal_places=2)),
                ('points', models.IntegerField(default=0)),
                ('victoire', models.IntegerField(default=0)),
                ('defaite', models.IntegerField(default=0)),
            ],
        ),
    ]
