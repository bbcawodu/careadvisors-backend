# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0066_auto_20180426_1754'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseManagementClient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='picmodels.Address')),
            ],
            options={
                'verbose_name_plural': 'Navigator Metrics Locations',
            },
        ),
        migrations.AlterUniqueTogether(
            name='casemanagementclient',
            unique_together=set([('address', 'name')]),
        ),
    ]
