# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0002_auto_20151014_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table_joueurs',
            name='points',
            field=models.IntegerField(default=b'0'),
        ),
    ]
