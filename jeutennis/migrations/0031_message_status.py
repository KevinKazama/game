# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0030_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
