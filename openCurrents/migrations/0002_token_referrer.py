# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-21 08:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('openCurrents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='referrer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
