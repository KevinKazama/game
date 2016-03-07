# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0025_auto_20151212_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='table_match',
            name='idtournoi',
            field=models.ForeignKey(default=1, blank=True, to='jeutennis.table_tournoi'),
            preserve_default=False,
        ),
    ]
