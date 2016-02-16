# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeutennis', '0024_auto_20151209_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='table_tournoi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=20)),
                ('participants', models.IntegerField(default=16)),
                ('date_tournoi', models.DateField()),
                ('winner', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='table_joueurs',
            name='idtournoi',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='table_match',
            name='winner',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
