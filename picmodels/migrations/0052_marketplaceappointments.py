# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0051_healthcareserviceexpertise'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketplaceAppointments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('date', models.DateField(null=True, blank=True)),
                ('start_time', models.TimeField(null=True, blank=True)),
                ('end_time', models.TimeField(null=True, blank=True)),
                ('consumer', models.ForeignKey(to='picmodels.PICConsumer', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True)),
                ('navigator', models.ForeignKey(to='picmodels.Navigators', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True)),
            ],
        ),
    ]
