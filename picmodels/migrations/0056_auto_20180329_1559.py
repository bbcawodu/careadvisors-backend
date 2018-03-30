# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0055_auto_20180318_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='navigators',
            name='healthcare_service_expertises',
            field=models.ManyToManyField(related_name='navigators_with_expertise', blank=True, to='picmodels.HealthcareServiceExpertise'),
        ),
    ]
