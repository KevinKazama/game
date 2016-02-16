# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0005_auto_20151014_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table_joueurs',
            name='points',
            field=models.IntegerField(default=0, null=0, blank=True),
        ),
    ]
