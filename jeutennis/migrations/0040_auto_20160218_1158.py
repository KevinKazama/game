# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0039_table_joueurs_date_vie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table_tournoi',
            name='winner',
        ),
        migrations.AddField(
            model_name='table_tournoi',
            name='wintour',
            field=models.ForeignKey(related_name='win_j1', default=1, to='jeutennis.table_joueurs'),
            preserve_default=False,
        ),
    ]
