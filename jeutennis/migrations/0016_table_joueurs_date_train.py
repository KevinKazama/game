# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0015_auto_20151019_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='table_joueurs',
            name='date_train',
            field=models.DateField(default=datetime.datetime(2015, 10, 20, 9, 34, 51, 133268, tzinfo=utc), verbose_name=b'train'),
            preserve_default=False,
        ),
    ]
