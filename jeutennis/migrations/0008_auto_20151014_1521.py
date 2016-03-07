# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0007_auto_20151014_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table_joueurs',
            name='concentration',
            field=models.DecimalField(default=0.0, max_digits=2, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='table_joueurs',
            name='defaite',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='table_joueurs',
            name='endurance',
            field=models.DecimalField(default=0.0, max_digits=2, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='table_joueurs',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='table_joueurs',
            name='retour',
            field=models.DecimalField(default=0.0, max_digits=2, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='table_joueurs',
            name='victoire',
            field=models.IntegerField(default=0),
        ),
    ]
