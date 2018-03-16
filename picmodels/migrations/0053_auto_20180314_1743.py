# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0052_marketplaceappointments'),
    ]

    operations = [
        migrations.AddField(
            model_name='picconsumer',
            name='billing_amount',
            field=models.DecimalField(decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], null=True, max_digits=14, blank=True),
        ),
        migrations.AddField(
            model_name='picconsumer',
            name='consumer_need',
            field=models.CharField(max_length=1000, null=True, choices=[('choose a doctor', 'choose a doctor'), ('billing issues', 'billing issues'), ('Not Available', 'Not Available')], blank=True, default='Not Available'),
        ),
        migrations.AddField(
            model_name='picconsumer',
            name='healthcare_networks_used',
            field=models.ManyToManyField(to='picmodels.ProviderNetwork', blank=True),
        ),
        migrations.AddField(
            model_name='picconsumer',
            name='insurance_carrier',
            field=models.ForeignKey(null=True, to='picmodels.HealthcareCarrier', blank=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='picconsumer',
            name='service_expertise_need',
            field=models.ForeignKey(null=True, to='picmodels.HealthcareServiceExpertise', blank=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='picconsumerbackup',
            name='billing_amount',
            field=models.DecimalField(decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], null=True, max_digits=14, blank=True),
        ),
        migrations.AddField(
            model_name='picconsumerbackup',
            name='consumer_need',
            field=models.CharField(max_length=1000, null=True, choices=[('choose a doctor', 'choose a doctor'), ('billing issues', 'billing issues'), ('Not Available', 'Not Available')], blank=True, default='Not Available'),
        ),
        migrations.AddField(
            model_name='picconsumerbackup',
            name='healthcare_networks_used',
            field=models.ManyToManyField(to='picmodels.ProviderNetwork', blank=True),
        ),
        migrations.AddField(
            model_name='picconsumerbackup',
            name='insurance_carrier',
            field=models.ForeignKey(null=True, to='picmodels.HealthcareCarrier', blank=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='picconsumerbackup',
            name='service_expertise_need',
            field=models.ForeignKey(null=True, to='picmodels.HealthcareServiceExpertise', blank=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
