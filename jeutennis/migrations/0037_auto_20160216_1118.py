# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0036_staff_table_equipement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table_joueurs',
            name='endurance',
            field=models.IntegerField(default=10),
        ),
    ]
