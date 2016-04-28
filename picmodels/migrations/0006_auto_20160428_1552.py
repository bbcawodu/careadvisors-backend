# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0005_auto_20160428_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picconsumer',
            name='navigator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='picmodels.PICStaff', null=True),
        ),
    ]
