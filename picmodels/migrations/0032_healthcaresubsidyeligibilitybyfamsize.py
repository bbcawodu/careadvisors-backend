# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0031_hospitalwebtrafficdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthcareSubsidyEligibilityByFamSize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('family_size', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('medicaid_income_limit', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('tax_cred_for_marketplace_income_limit', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('marketplace_without_subsidies_income_level', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
            ],
        ),
    ]
