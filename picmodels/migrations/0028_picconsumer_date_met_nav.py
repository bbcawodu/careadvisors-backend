# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0027_auto_20161129_0246'),
    ]

    operations = [
        migrations.AddField(
            model_name='picconsumer',
            name='date_met_nav',
            field=models.DateField(null=True, blank=True),
        ),
    ]
