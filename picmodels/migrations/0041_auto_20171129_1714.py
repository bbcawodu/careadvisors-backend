# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0040_auto_20170808_1541'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumerHospitalInfo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('treatment_site', models.CharField(blank=True, max_length=1000, null=True)),
                ('account_number', models.CharField(blank=True, max_length=1000, null=True)),
                ('mrn', models.CharField(blank=True, max_length=1000, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('ssn', models.CharField(blank=True, max_length=10, null=True)),
                ('state', models.CharField(blank=True, max_length=5, null=True)),
                ('p_class', models.CharField(blank=True, max_length=100, null=True)),
                ('admit_date', models.DateField(blank=True, null=True)),
                ('discharge_date', models.DateField(blank=True, null=True)),
                ('medical_charges', models.FloatField(blank=True, null=True)),
                ('referred_date', models.DateField(blank=True, null=True)),
                ('no_date', models.DateField(blank=True, null=True)),
                ('type', models.CharField(blank=True, max_length=1000, null=True)),
                ('no_reason', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='picconsumer',
            name='consumer_hospital_info',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, to='picmodels.ConsumerHospitalInfo', null=True),
        ),
        migrations.AddField(
            model_name='picconsumerbackup',
            name='consumer_hospital_info',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, to='picmodels.ConsumerHospitalInfo', null=True),
        ),
    ]
