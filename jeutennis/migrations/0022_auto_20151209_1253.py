# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0021_auto_20151209_1220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='j1',
        ),
        migrations.RemoveField(
            model_name='match',
            name='j2',
        ),
        migrations.DeleteModel(
            name='match',
        ),
    ]
