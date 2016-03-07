# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0020_match'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='s2j2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='s3j2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='s4j2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='s5j2',
            field=models.IntegerField(default=0),
        ),
    ]
