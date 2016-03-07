# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0026_table_match_idtournoi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table_tournoi',
            name='date_tournoi',
            field=models.DateTimeField(),
        ),
    ]
