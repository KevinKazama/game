# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0028_table_joueurs_tirage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table_joueurs',
            name='tirage',
        ),
        migrations.AddField(
            model_name='table_tournoi',
            name='tirage',
            field=models.IntegerField(default=0),
        ),
    ]
