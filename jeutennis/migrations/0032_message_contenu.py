# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0031_message_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='contenu',
            field=models.TextField(default='test'),
            preserve_default=False,
        ),
    ]
