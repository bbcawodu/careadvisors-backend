# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0024_consumergeneralconcern_consumerspecificconcern'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthcarecarrier',
            name='sample_id_card',
            field=models.ImageField(upload_to='carrier_sample_id_cards/', default='carrier_sample_id_cards/None/default_sample_id_card.jpg'),
        ),
    ]
