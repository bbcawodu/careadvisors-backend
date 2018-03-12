# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0050_auto_20180306_1502'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthcareServiceExpertise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=1000)),
            ],
        ),
    ]
