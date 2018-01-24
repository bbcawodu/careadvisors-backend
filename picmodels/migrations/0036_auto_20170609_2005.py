# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import picmodels.models.care_advisors.providers_plan_network_models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0035_auto_20170609_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calltoaction',
            name='cta_image',
            field=models.ImageField(blank=True, null=True, upload_to=picmodels.models.care_advisors.call_to_action_models.get_cta_image_file_path),
        ),
        migrations.AlterField(
            model_name='healthcarecarrier',
            name='sample_id_card',
            field=models.ImageField(blank=True, null=True, upload_to=picmodels.models.care_advisors.providers_plan_network_models.get_sample_id_card_file_path),
        ),
    ]
