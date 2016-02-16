# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0029_auto_20160129_1205'),
    ]

    operations = [
        migrations.CreateModel(
            name='message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dest', models.ForeignKey(related_name='dest', to='jeutennis.table_joueurs')),
                ('emetteur', models.ForeignKey(related_name='emetteur', to='jeutennis.table_joueurs')),
            ],
        ),
    ]
