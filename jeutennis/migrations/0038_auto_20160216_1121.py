# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0037_auto_20160216_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='table_joueurs',
            name='vie',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='table_joueurs',
            name='endurance',
            field=models.IntegerField(default=0),
        ),
    ]
