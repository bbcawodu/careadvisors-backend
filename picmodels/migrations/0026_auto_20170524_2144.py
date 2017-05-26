# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0025_healthcarecarrier_sample_id_card'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthcareServiceCostEntry',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('cost_relation_to_deductible', models.CharField(choices=[('Before', 'Before'), ('After', 'After')], null=True, max_length=100, blank=True)),
                ('coinsurance', models.FloatField(default=0.0, validators=[django.core.validators.MaxValueValidator(100)])),
                ('copay', models.FloatField(default=0.0)),
            ],
        ),
        migrations.AddField(
            model_name='healthcareplan',
            name='medical_deductible_family_standard',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='healthcareplan',
            name='medical_deductible_individual_standard',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='healthcareplan',
            name='medical_out_of_pocket_max_family_standard',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='healthcareplan',
            name='medical_out_of_pocket_max_individual_standard',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='healthcareplan',
            name='emergency_room_standard_cost',
            field=models.ForeignKey(to='picmodels.HealthcareServiceCostEntry', null=True, blank=True, related_name='plan_instance_for_emergency_room_standard_cost', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='healthcareplan',
            name='generic_drugs_standard_cost',
            field=models.ForeignKey(to='picmodels.HealthcareServiceCostEntry', null=True, blank=True, related_name='plan_instance_for_generic_drugs_standard_cost', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='healthcareplan',
            name='inpatient_facility_standard_cost',
            field=models.ForeignKey(to='picmodels.HealthcareServiceCostEntry', null=True, blank=True, related_name='plan_instance_for_inpatient_facility_standard_cost', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='healthcareplan',
            name='non_preferred_brand_drugs_standard_cost',
            field=models.ForeignKey(to='picmodels.HealthcareServiceCostEntry', null=True, blank=True, related_name='plan_instance_for_non_preferred_brand_drugs_standard_cost', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='healthcareplan',
            name='preferred_brand_drugs_standard_cost',
            field=models.ForeignKey(to='picmodels.HealthcareServiceCostEntry', null=True, blank=True, related_name='plan_instance_for_preferred_brand_drugs_standard_cost', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='healthcareplan',
            name='primary_care_physician_family_standard_cost',
            field=models.ForeignKey(to='picmodels.HealthcareServiceCostEntry', null=True, blank=True, related_name='plan_instance_for_primary_care_physician_family_standard_cost', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='healthcareplan',
            name='primary_care_physician_individual_standard_cost',
            field=models.ForeignKey(to='picmodels.HealthcareServiceCostEntry', null=True, blank=True, related_name='plan_instance_for_primary_care_physician_individual_standard_cost', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='healthcareplan',
            name='specialist_standard_cost',
            field=models.ForeignKey(to='picmodels.HealthcareServiceCostEntry', null=True, blank=True, related_name='plan_instance_for_specialist_standard_cost', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='healthcareplan',
            name='specialty_drugs_standard_cost',
            field=models.ForeignKey(to='picmodels.HealthcareServiceCostEntry', null=True, blank=True, related_name='plan_instance_for_specialty_drugs_standard_cost', on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
