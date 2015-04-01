# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created', models.DateField(default=datetime.datetime(2015, 3, 31, 19, 35, 6, 260552))),
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
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created', models.DateField(default=datetime.datetime(2015, 3, 31, 19, 35, 6, 260552))),
                ('active', models.BooleanField(default='true')),
                ('code', models.CharField(unique=True, max_length=10, null=True)),
                ('name', models.CharField(max_length=100)),
                ('firebase_path', models.CharField(unique=True, max_length=64, null=True)),
                ('firebase_user', models.CharField(max_length=50, null=True)),
                ('firebase_password', models.CharField(max_length=20, null=True)),
                ('firebase_token', models.CharField(max_length=64, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='member',
            name='team',
            field=models.ForeignKey(to='teams.Team', related_name='members'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='administrator',
            name='team',
            field=models.ForeignKey(to='teams.Team', related_name='administrators'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='administrator',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
