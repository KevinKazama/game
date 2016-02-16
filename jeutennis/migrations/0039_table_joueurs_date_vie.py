# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0038_auto_20160216_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='table_joueurs',
            name='date_vie',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 11, 44, 3, 79702, tzinfo=utc), verbose_name=b'dvie'),
            preserve_default=False,
        ),
    ]
