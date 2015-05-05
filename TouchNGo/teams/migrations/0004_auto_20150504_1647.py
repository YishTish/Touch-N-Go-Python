# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_auto_20150331_1950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='administrator',
            name='team',
        ),
        migrations.AddField(
            model_name='administrator',
            name='teams',
            field=models.ManyToManyField(to='teams.Team'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='created',
            field=models.DateField(default=datetime.datetime(2015, 5, 4, 16, 47, 58, 101696)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='udid',
            field=models.CharField(unique=True, max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='team',
            name='created',
            field=models.DateField(default=datetime.datetime(2015, 5, 4, 16, 47, 58, 101696)),
            preserve_default=True,
        ),
    ]
