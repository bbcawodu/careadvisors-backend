# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0007_auto_20160510_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metricssubmission',
            name='county',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='metricssubmission',
            name='outreach_activity',
            field=models.CharField(default='', null=True, blank=True, max_length=5000),
        ),
        migrations.AlterField(
            model_name='metricssubmission',
            name='trends',
            field=models.CharField(default='', null=True, blank=True, max_length=5000),
        ),
        migrations.AlterField(
            model_name='metricssubmission',
            name='zipcode',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='picconsumer',
            name='last_name',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='picconsumer',
            name='zipcode',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='picstaff',
            name='county',
            field=models.CharField(default='', null=True, blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='picstaff',
            name='last_name',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='planstat',
            name='metal_level',
            field=models.CharField(default='Not Available', null=True, choices=[('Bronze', 'Bronze'), ('Silver', 'Silver'), ('Gold', 'Gold'), ('Catastrophic', 'Catastrophic'), ('Not Available', 'Not Available')], blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='planstat',
            name='plan_name',
            field=models.CharField(default='Miscellaneous', choices=[('All Savers Insurance Company', 'All Savers Insurance Company'), ('CareSource Indiana, Inc.', 'CareSource Indiana, Inc.'), ('Humana Health Plan, Inc.', 'Humana Health Plan, Inc.'), ('Health Alliance Medical Plans, Inc.', 'Health Alliance Medical Plans, Inc.'), ('Blue Cross Blue Shield of Illinois', 'Blue Cross Blue Shield of Illinois'), ('Coventry Health Care of Illinois, Inc.', 'Coventry Health Care of Illinois, Inc.'), ('Coventry Health & Life Co.', 'Coventry Health & Life Co.'), ('United Healthcare of the Midwest, Inc.', 'United Healthcare of the Midwest, Inc.'), ('Celtic Insurance Company', 'Celtic Insurance Company'), ('Harken Health Insurance Company', 'Harken Health Insurance Company'), ('Aetna Health Inc.', 'Aetna Health Inc.'), ('Southeastern Indiana Health Organization', 'Southeastern Indiana Health Organization'), ('Anthem Ins Companies Inc(Anthem BCBS)', 'Anthem Ins Companies Inc(Anthem BCBS)'), ('Physicians Health Plan of Northern Indiana, Inc.', 'Physicians Health Plan of Northern Indiana, Inc.'), ('MDwise Marketplace, Inc.', 'MDwise Marketplace, Inc.'), ('Indiana University Health Plans, Inc.', 'Indiana University Health Plans, Inc.'), ('Miscellaneous', 'Miscellaneous')], max_length=1000),
        ),
        migrations.AlterField(
            model_name='planstat',
            name='premium_type',
            field=models.CharField(default='Not Available', null=True, choices=[('HMO', 'HMO'), ('PPO', 'PPO'), ('Not Available', 'Not Available')], blank=True, max_length=1000),
        ),
    ]
