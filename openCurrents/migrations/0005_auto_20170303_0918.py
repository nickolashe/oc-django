# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-03 09:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openCurrents', '0004_auto_20170303_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='org',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='org',
            name='mission',
            field=models.CharField(max_length=4096, null=True),
        ),
        migrations.AlterField(
            model_name='org',
            name='reason',
            field=models.CharField(max_length=4096, null=True),
        ),
    ]
