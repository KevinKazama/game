# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0014_table_joueurs_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table_joueurs',
            name='concentration',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='table_joueurs',
            name='endurance',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='table_joueurs',
            name='retour',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='table_joueurs',
            name='service',
            field=models.IntegerField(default=0),
        ),
    ]
