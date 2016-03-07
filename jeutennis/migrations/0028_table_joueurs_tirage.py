# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0027_auto_20151213_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='table_joueurs',
            name='tirage',
            field=models.IntegerField(default=0),
        ),
    ]
