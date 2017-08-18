# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-08-07 20:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openCurrents', '0036_auto_20170804_0632'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='creator_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='notified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='org',
            name='website',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
