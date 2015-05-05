# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_auto_20150504_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='created',
            field=models.DateField(default=datetime.datetime(2015, 5, 5, 15, 22, 34, 785240)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='team',
            name='created',
            field=models.DateField(default=datetime.datetime(2015, 5, 5, 15, 22, 34, 785240)),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together=set([('team', 'phone_number')]),
        ),
    ]
