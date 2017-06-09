# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0033_auto_20170609_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calltoaction',
            name='cta_image',
            field=models.ImageField(blank=True, upload_to='call_to_actions/', null=True),
        ),
        migrations.AlterField(
            model_name='healthcarecarrier',
            name='sample_id_card',
            field=models.ImageField(blank=True, upload_to='carrier_sample_id_cards/', null=True),
        ),
    ]
