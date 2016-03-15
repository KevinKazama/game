# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0043_auto_20160306_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='table_equipement',
            name='nivreq',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='table_joueurs',
            name='exp',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='table_joueurs',
            name='niveau',
            field=models.IntegerField(default=1),
        ),
    ]
