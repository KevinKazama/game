# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0042_auto_20160306_2238'),
    ]

    operations = [
        migrations.AddField(
            model_name='table_equipement',
            name='nom',
            field=models.CharField(default='Raquette de novice', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='table_equipement',
            name='proprio',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='table_joueurs',
            name='is_equip',
            field=models.ForeignKey(default=1, to='jeutennis.table_equipement'),
            preserve_default=False,
        ),
    ]
