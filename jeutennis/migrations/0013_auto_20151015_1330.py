# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0012_auto_20151015_0009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table_joueurs',
            name='adresse',
        ),
        migrations.RemoveField(
            model_name='table_joueurs',
            name='date_insc',
        ),
        migrations.RemoveField(
            model_name='table_joueurs',
            name='motdepasse',
        ),
        migrations.RemoveField(
            model_name='table_joueurs',
            name='pseudo',
        ),
    ]
