# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0046_table_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='table_equipement',
            name='nivreq',
            field=models.ForeignKey(default=1, to='jeutennis.table_level'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='table_joueurs',
            name='niveau',
            field=models.ForeignKey(default=1, to='jeutennis.table_level'),
            preserve_default=False,
        ),
    ]
