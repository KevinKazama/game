# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0018_table_joueurs_date_match'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table_joueurs',
            name='date_match',
            field=models.DateTimeField(verbose_name=b'match'),
        ),
    ]
