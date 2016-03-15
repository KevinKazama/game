# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0044_auto_20160306_2252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table_equipement',
            name='nivreq',
        ),
        migrations.RemoveField(
            model_name='table_joueurs',
            name='niveau',
        ),
    ]
