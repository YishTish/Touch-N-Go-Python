# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='administrator',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateField(default=datetime.datetime(2015, 3, 12, 17, 3, 18, 808862))),
                ('active', models.BooleanField(default='true')),
                ('name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='member',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateField(default=datetime.datetime(2015, 3, 12, 17, 3, 18, 808862))),
                ('active', models.BooleanField(default='true')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('udid', models.CharField(max_length=40)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='team',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateField(default=datetime.datetime(2015, 3, 12, 17, 3, 18, 808862))),
                ('active', models.BooleanField(default='true')),
                ('team_code', models.CharField(max_length=65)),
                ('name', models.CharField(max_length=100)),
                ('firebase_secret', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='member',
            name='team_code',
            field=models.ForeignKey(to='teams.team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='administrator',
            name='team',
            field=models.ForeignKey(to='teams.team'),
            preserve_default=True,
        ),
    ]
