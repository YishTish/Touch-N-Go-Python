# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='created',
            field=models.DateField(default=datetime.datetime(2015, 3, 31, 19, 35, 30, 432594)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='team',
            name='created',
            field=models.DateField(default=datetime.datetime(2015, 3, 31, 19, 35, 30, 432594)),
            preserve_default=True,
        ),
    ]
