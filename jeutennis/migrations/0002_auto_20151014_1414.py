# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table_joueurs',
            name='service',
            field=models.DecimalField(default=0.0, max_digits=2, decimal_places=2),
        ),
    ]
