# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0016_table_joueurs_date_train'),
    ]

    operations = [
        migrations.AddField(
            model_name='table_joueurs',
            name='adversaire',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
    ]
