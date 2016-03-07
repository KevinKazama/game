# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0040_auto_20160218_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='table_joueurs',
            name='is_equip',
            field=models.IntegerField(default=0),
        ),
    ]
