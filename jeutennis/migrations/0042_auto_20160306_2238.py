# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0041_table_joueurs_is_equip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table_equipement',
            name='proprio',
        ),
        migrations.RemoveField(
            model_name='table_joueurs',
            name='is_equip',
        ),
    ]
