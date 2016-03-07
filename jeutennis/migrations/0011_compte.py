# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0010_auto_20151014_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compte',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pseudo', models.CharField(max_length=15)),
                ('adresse', models.CharField(max_length=30)),
                ('motdepasse', models.CharField(max_length=30)),
                ('date_insc', models.DateField(verbose_name=b'inscription')),
                ('compte', models.ForeignKey(to='jeutennis.table_joueurs')),
            ],
        ),
    ]
