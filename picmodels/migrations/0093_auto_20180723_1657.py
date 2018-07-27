# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0092_auto_20180720_1855'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumerHospitalData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('medical_record_number', models.CharField(max_length=5000, blank=True, null=True)),
                ('discharge_date', models.DateField(blank=True, null=True)),
                ('billing_amount', models.DecimalField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], max_digits=14, decimal_places=2)),
                ('hospital_name', models.CharField(max_length=5000, blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='picconsumer',
            name='consumer_hospital_info',
        ),
        migrations.RemoveField(
            model_name='picconsumerbackup',
            name='consumer_hospital_info',
        ),
        migrations.DeleteModel(
            name='ConsumerHospitalInfo',
        ),
        migrations.AddField(
            model_name='picconsumer',
            name='consumer_hospital_data',
            field=models.ForeignKey(blank=True, null=True, related_name='consumers_attached_to_this_hospital_data', on_delete=django.db.models.deletion.SET_NULL, to='picmodels.ConsumerHospitalData'),
        ),
        migrations.AddField(
            model_name='picconsumerbackup',
            name='consumer_hospital_data',
            field=models.ForeignKey(blank=True, null=True, related_name='backup_consumers_attached_to_this_hospital_data', on_delete=django.db.models.deletion.SET_NULL, to='picmodels.ConsumerHospitalData'),
        ),
    ]
