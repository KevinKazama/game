# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0033_auto_20160214_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='table_joueurs',
            name='argent',
            field=models.IntegerField(default=1000),
        ),
        migrations.AddField(
            model_name='table_joueurs',
            name='coffre',
            field=models.IntegerField(default=0),
        ),
    ]
