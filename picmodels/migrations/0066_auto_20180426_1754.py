# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import picmodels.models.care_advisors.healthcare_provider_coverage_network_models.coverage_carrier_models.models
import custom_storages
import picmodels.models.care_advisors.call_to_action_models.models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0065_auto_20180426_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calltoaction',
            name='cta_image',
            field=models.ImageField(blank=True, null=True, upload_to=picmodels.models.care_advisors.call_to_action_models.get_cta_image_file_path, storage=custom_storages.PublicMediaStorage()),
        ),
        migrations.AlterField(
            model_name='healthcarecarrier',
            name='sample_id_card',
            field=models.ImageField(blank=True, null=True, upload_to=picmodels.models.care_advisors.healthcare_provider_coverage_network_models.coverage_carrier_models.get_sample_id_card_file_path, storage=custom_storages.PublicMediaStorage()),
        ),
    ]
