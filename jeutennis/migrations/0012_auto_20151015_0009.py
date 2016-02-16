# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0011_compte'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compte',
            name='compte',
        ),
        migrations.AddField(
            model_name='table_joueurs',
            name='adresse',
            field=models.CharField(default='test', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='table_joueurs',
            name='date_insc',
            field=models.DateField(default=datetime.datetime(2015, 10, 14, 22, 9, 22, 145490, tzinfo=utc), verbose_name=b'inscription'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='table_joueurs',
            name='motdepasse',
            field=models.CharField(default=123, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='table_joueurs',
            name='pseudo',
            field=models.CharField(default='test', max_length=15),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Compte',
        ),
    ]
