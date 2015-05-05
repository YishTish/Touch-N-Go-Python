# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_auto_20150504_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='created',
            field=models.DateField(default=datetime.datetime(2015, 5, 4, 17, 24, 55, 147980)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='udid',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='team',
            name='created',
            field=models.DateField(default=datetime.datetime(2015, 5, 4, 17, 24, 55, 147980)),
            preserve_default=True,
        ),
    ]
