# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0020_auto_20160328_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='planstat',
            name='metal_level',
            field=models.CharField(default=b'Not Available', max_length=1000, blank=True, choices=[(b'Bronze', b'Bronze'), (b'Silver', b'Silver'), (b'Gold', b'Gold'), (b'Catastrophic', b'Catastrophic'), (b'Not Available', b'Not Available')]),
        ),
        migrations.AddField(
            model_name='planstat',
            name='premium_type',
            field=models.CharField(default=b'Not Available', max_length=1000, blank=True, choices=[(b'HMO', b'HMO'), (b'PPO', b'PP0'), (b'Not Available', b'Not Available')]),
        ),
        migrations.AlterField(
            model_name='planstat',
            name='plan_name',
            field=models.CharField(default=b'Miscellaneous', max_length=1000, choices=[(b'All Savers Insurance Company', b'All Savers Insurance Company'), (b'CareSource Indiana, Inc.', b'CareSource Indiana, Inc.'), (b'Humana Health Plan, Inc.', b'Humana Health Plan, Inc.'), (b'Health Alliance Medical Plans, Inc.', b'Health Alliance Medical Plans, Inc.'), (b'Blue Cross Blue Shield of Illinois', b'Blue Cross Blue Shield of Illinois'), (b'Coventry Health Care of Illinois, Inc.', b'Coventry Health Care of Illinois, Inc.'), (b'Coventry Health & Life Co.', b'Coventry Health & Life Co.'), (b'United Healthcare of the Midwest, Inc.', b'United Healthcare of the Midwest, Inc.'), (b'Celtic Insurance Company', b'Celtic Insurance Company'), (b'Harken Health Insurance Company', b'Harken Health Insurance Company'), (b'Aetna Health Inc.', b'Aetna Health Inc.'), (b'Southeastern Indiana Health Organization', b'Southeastern Indiana Health Organization'), (b'Anthem Ins Companies Inc(Anthem BCBS)', b'Anthem Ins Companies Inc(Anthem BCBS)'), (b'Physicians Health Plan of Northern Indiana, Inc.', b'Physicians Health Plan of Northern Indiana, Inc.'), (b'MDwise Marketplace, Inc.', b'MDwise Marketplace, Inc.'), (b'Indiana University Health Plans, Inc.', b'Indiana University Health Plans, Inc.'), (b'Miscellaneous', b'Miscellaneous')]),
        ),
    ]
