# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-02-07 06:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import openCurrents.interfaces.common
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminActionUserTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(choices=[('app', 'approved'), ('dec', 'declined'), ('req', 'approval_request')], max_length=3)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=8192)),
                ('location', models.CharField(max_length=1024)),
                ('creator_id', models.IntegerField(default=0)),
                ('notified', models.BooleanField(default=False)),
                ('event_type', models.CharField(choices=[('MN', 'ManualTracking'), ('GR', 'Group')], default='GR', max_length=2)),
                ('is_public', models.BooleanField(default=False)),
                ('datetime_start', models.DateTimeField(verbose_name='start datetime')),
                ('datetime_end', models.DateTimeField(verbose_name='end datetime')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('coordinator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['datetime_start'],
                'get_latest_by': 'datetime_start',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Ledger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('cur', 'current'), ('usd', 'dollar')], default='cur', max_length=3)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('is_issued', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('action', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='openCurrents.AdminActionUserTime')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_master', models.BooleanField(default=False)),
                ('currents_share', models.IntegerField()),
                ('limit', models.IntegerField(default=-1)),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='openCurrents.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Org',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(max_length=10, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('address', models.CharField(max_length=1024, null=True)),
                ('intro', models.CharField(max_length=16192, null=True)),
                ('status', models.CharField(choices=[('biz', 'business'), ('npf', 'non-profit')], default='npf', max_length=3)),
                ('timezone', models.CharField(default='America/Chicago', max_length=128)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
            ],
        ),
        migrations.CreateModel(
            name='OrgUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('affiliation', models.CharField(max_length=50, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='openCurrents.Org')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='openCurrents.Org')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='openCurrents.Event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('is_verified', models.BooleanField(default=False)),
                ('token', models.UUIDField(default=uuid.uuid4)),
                ('token_type', models.CharField(max_length=20)),
                ('date_expires', models.DateTimeField(default=openCurrents.interfaces.common.one_week_from_now, verbose_name='date invite token expires')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('referrer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'date_created',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pop_image', models.ImageField(null=True, upload_to='images/redeem/%Y/%m/%d')),
                ('pop_no_proof', models.CharField(max_length=8096, null=True)),
                ('pop_type', models.CharField(choices=[('rec', 'receipt'), ('oth', 'other')], default='rec', max_length=3)),
                ('price_reported', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_actual', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currents_amount', models.DecimalField(decimal_places=3, max_digits=12)),
                ('biz_name', models.CharField(max_length=256, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='openCurrents.Offer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(choices=[('req', 'pending'), ('app', 'approved'), ('red', 'redeemed'), ('dec', 'declined')], default='req', max_length=7)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='openCurrents.Transaction')),
            ],
            options={
                'get_latest_by': 'date_updated',
            },
        ),
        migrations.CreateModel(
            name='UserEventRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_confirmed', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='openCurrents.Event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timezone', models.CharField(default='America/Chicago', max_length=128)),
                ('monthly_updates', models.BooleanField(default=False)),
                ('popup_reaction', models.NullBooleanField(default=None)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date last updated')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserTimeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_verified', models.BooleanField(default=False)),
                ('datetime_start', models.DateTimeField(verbose_name='start time')),
                ('datetime_end', models.DateTimeField(blank=True, null=True, verbose_name='end time')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('deferments', models.ManyToManyField(related_name='deferments', through='openCurrents.AdminActionUserTime', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='openCurrents.Event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'datetime_start',
            },
        ),
        migrations.CreateModel(
            name='OrgEntity',
            fields=[
                ('entity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='openCurrents.Entity')),
            ],
            bases=('openCurrents.entity',),
        ),
        migrations.CreateModel(
            name='UserEntity',
            fields=[
                ('entity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='openCurrents.Entity')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('openCurrents.entity',),
        ),
        migrations.AddField(
            model_name='org',
            name='users',
            field=models.ManyToManyField(through='openCurrents.OrgUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='offer',
            name='org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='openCurrents.Org'),
        ),
        migrations.AddField(
            model_name='ledger',
            name='entity_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_out', to='openCurrents.Entity'),
        ),
        migrations.AddField(
            model_name='ledger',
            name='entity_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_in', to='openCurrents.Entity'),
        ),
        migrations.AddField(
            model_name='ledger',
            name='transaction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='openCurrents.TransactionAction'),
        ),
        migrations.AddField(
            model_name='event',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='openCurrents.Project'),
        ),
        migrations.AddField(
            model_name='adminactionusertime',
            name='usertimelog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='openCurrents.UserTimeLog'),
        ),
        migrations.AlterUniqueTogether(
            name='usertimelog',
            unique_together=set([('user', 'event')]),
        ),
        migrations.AlterUniqueTogether(
            name='usereventregistration',
            unique_together=set([('user', 'event')]),
        ),
        migrations.AlterUniqueTogether(
            name='transactionaction',
            unique_together=set([('transaction', 'action_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='orguser',
            unique_together=set([('user', 'org')]),
        ),
        migrations.AddField(
            model_name='orgentity',
            name='org',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='openCurrents.Org'),
        ),
        migrations.AlterUniqueTogether(
            name='adminactionusertime',
            unique_together=set([('action_type', 'user', 'usertimelog')]),
        ),
    ]
