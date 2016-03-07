# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0032_message_contenu'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='date_mp',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 14, 10, 6, 57, 525270, tzinfo=utc), verbose_name=b'mp'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='sujet',
            field=models.CharField(default='test2', max_length=25),
            preserve_default=False,
        ),
    ]
