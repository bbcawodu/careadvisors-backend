# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0032_healthcaresubsidyeligibilitybyfamsize'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calltoaction',
            name='cta_image',
            field=models.ImageField(upload_to='call_to_actions/', default='call_to_actions/None/default_cta_image.jpg'),
        ),
        migrations.AlterField(
            model_name='healthcarecarrier',
            name='sample_id_card',
            field=models.ImageField(upload_to='carrier_sample_id_cards/', default='carrier_sample_id_cards/None/default_sample_id_card_image.jpg'),
        ),
        migrations.AlterField(
            model_name='picstaff',
            name='staff_pic',
            field=models.ImageField(upload_to='staff_pics/', blank=True, null=True),
        ),
    ]
