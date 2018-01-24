# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0046_cpsmetricssubmission_metricsplanstatistic'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseManagementStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('date_created', models.DateTimeField(null=True, auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('management_step', models.IntegerField()),
                ('management_notes', models.TextField(null=True, blank=True)),
                ('contact', models.ForeignKey(null=True, blank=True, to='picmodels.PICConsumer')),
            ],
        ),
    ]
