# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0045_auto_20160307_1211'),
    ]

    operations = [
        migrations.CreateModel(
            name='table_level',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('min_exp', models.IntegerField(default=0)),
                ('max_exp', models.IntegerField(default=1)),
                ('nargent', models.IntegerField(default=1)),
                ('nvictoire', models.IntegerField(default=1)),
            ],
        ),
    ]
