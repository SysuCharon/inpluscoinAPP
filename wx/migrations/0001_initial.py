# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('txid', models.CharField(max_length=70)),
                ('count', models.CharField(max_length=3)),
                ('sub', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('openID', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name='content',
            name='user',
            field=models.ForeignKey(to='wx.User'),
        ),
    ]
