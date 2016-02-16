# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0034_auto_20160215_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='crypt',
            field=models.CharField(default='azerty', max_length=6),
            preserve_default=False,
        ),
    ]
