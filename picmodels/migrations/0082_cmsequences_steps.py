# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0081_testenrollmentstep'),
    ]

    operations = [
        migrations.AddField(
            model_name='cmsequences',
            name='steps',
            field=models.ManyToManyField(blank=True, null=True, to='picmodels.StepsForCMSequences'),
        ),
    ]
