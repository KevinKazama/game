# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0022_auto_20151209_1253'),
    ]

    operations = [
        migrations.CreateModel(
            name='match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('s1j1', models.IntegerField(default=0)),
                ('s2j1', models.IntegerField(default=0)),
                ('s3j1', models.IntegerField(default=0)),
                ('s4j1', models.IntegerField(default=0)),
                ('s5j1', models.IntegerField(default=0)),
                ('s1j2', models.IntegerField(default=0)),
                ('s2j2', models.IntegerField(default=0)),
                ('s3j2', models.IntegerField(default=0)),
                ('s4j2', models.IntegerField(default=0)),
                ('s5j2', models.IntegerField(default=0)),
                ('date_match', models.DateTimeField(verbose_name=b'match')),
                ('j1', models.ForeignKey(related_name='table_j1', to='jeutennis.table_joueurs')),
                ('j2', models.ForeignKey(related_name='table_j2', to='jeutennis.table_joueurs')),
            ],
        ),
    ]
