# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0026_auto_20170524_2144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='healthcareplan',
            name='emergency_room_standard_cost',
        ),
        migrations.RemoveField(
            model_name='healthcareplan',
            name='generic_drugs_standard_cost',
        ),
        migrations.RemoveField(
            model_name='healthcareplan',
            name='inpatient_facility_standard_cost',
        ),
        migrations.RemoveField(
            model_name='healthcareplan',
            name='non_preferred_brand_drugs_standard_cost',
        ),
        migrations.RemoveField(
            model_name='healthcareplan',
            name='preferred_brand_drugs_standard_cost',
        ),
        migrations.RemoveField(
            model_name='healthcareplan',
            name='primary_care_physician_family_standard_cost',
        ),
        migrations.RemoveField(
            model_name='healthcareplan',
            name='primary_care_physician_individual_standard_cost',
        ),
        migrations.RemoveField(
            model_name='healthcareplan',
            name='specialist_standard_cost',
        ),
        migrations.RemoveField(
            model_name='healthcareplan',
            name='specialty_drugs_standard_cost',
        ),
        migrations.AddField(
            model_name='healthcareservicecostentry',
            name='plan_obj_for_emergency_room_standard_cost',
            field=models.ForeignKey(blank=True, related_name='emergency_room_standard_cost', null=True, to='picmodels.HealthcarePlan'),
        ),
        migrations.AddField(
            model_name='healthcareservicecostentry',
            name='plan_obj_for_generic_drugs_standard_cost',
            field=models.ForeignKey(blank=True, related_name='generic_drugs_standard_cost', null=True, to='picmodels.HealthcarePlan'),
        ),
        migrations.AddField(
            model_name='healthcareservicecostentry',
            name='plan_obj_for_inpatient_facility_standard_cost',
            field=models.ForeignKey(blank=True, related_name='inpatient_facility_standard_cost', null=True, to='picmodels.HealthcarePlan'),
        ),
        migrations.AddField(
            model_name='healthcareservicecostentry',
            name='plan_obj_for_non_preferred_brand_drugs_standard_cost',
            field=models.ForeignKey(blank=True, related_name='non_preferred_brand_drugs_standard_cost', null=True, to='picmodels.HealthcarePlan'),
        ),
        migrations.AddField(
            model_name='healthcareservicecostentry',
            name='plan_obj_for_preferred_brand_drugs_standard_cost',
            field=models.ForeignKey(blank=True, related_name='preferred_brand_drugs_standard_cost', null=True, to='picmodels.HealthcarePlan'),
        ),
        migrations.AddField(
            model_name='healthcareservicecostentry',
            name='plan_obj_for_primary_care_physician_family_standard_cost',
            field=models.ForeignKey(blank=True, related_name='primary_care_physician_family_standard_cost', null=True, to='picmodels.HealthcarePlan'),
        ),
        migrations.AddField(
            model_name='healthcareservicecostentry',
            name='plan_obj_for_primary_care_physician_individual_standard_cost',
            field=models.ForeignKey(blank=True, related_name='primary_care_physician_individual_standard_cost', null=True, to='picmodels.HealthcarePlan'),
        ),
        migrations.AddField(
            model_name='healthcareservicecostentry',
            name='plan_obj_for_specialist_standard_cost',
            field=models.ForeignKey(blank=True, related_name='specialist_standard_cost', null=True, to='picmodels.HealthcarePlan'),
        ),
        migrations.AddField(
            model_name='healthcareservicecostentry',
            name='plan_obj_for_specialty_drugs_standard_cost',
            field=models.ForeignKey(blank=True, related_name='specialty_drugs_standard_cost', null=True, to='picmodels.HealthcarePlan'),
        ),
    ]
