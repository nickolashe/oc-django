# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-20 07:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openCurrents', '0078_offer_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='is_master',
            field=models.BooleanField(default=False),
        ),
    ]
