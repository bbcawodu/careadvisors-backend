# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0038_auto_20170714_1904'),
    ]

    operations = [
        migrations.CreateModel(
            name='CareAdvisorCustomer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('company_name', models.TextField()),
                ('phone_number', models.TextField()),
            ],
        ),
    ]
