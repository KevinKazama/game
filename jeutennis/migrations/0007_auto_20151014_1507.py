# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0006_auto_20151014_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table_joueurs',
            name='defaite',
            field=models.IntegerField(default=b'0'),
        ),
        migrations.AlterField(
            model_name='table_joueurs',
            name='points',
            field=models.IntegerField(default=b'0'),
        ),
        migrations.AlterField(
            model_name='table_joueurs',
            name='victoire',
            field=models.IntegerField(default=b'0'),
        ),
    ]
