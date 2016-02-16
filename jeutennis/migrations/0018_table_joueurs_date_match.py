# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0017_table_joueurs_adversaire'),
    ]

    operations = [
        migrations.AddField(
            model_name='table_joueurs',
            name='date_match',
            field=models.DateField(default=datetime.datetime(2015, 10, 20, 14, 38, 22, 596786, tzinfo=utc), verbose_name=b'match'),
            preserve_default=False,
        ),
    ]
