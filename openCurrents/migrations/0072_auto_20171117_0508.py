# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-17 05:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('openCurrents', '0071_ledger_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledger',
            name='action',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='openCurrents.AdminActionUserTime'),
        ),
    ]
