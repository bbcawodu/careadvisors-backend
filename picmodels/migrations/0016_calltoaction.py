# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0015_metricssubmission_no_cps_consumers'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallToAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('intent', models.CharField(max_length=1000)),
                ('cta_image', models.ImageField(upload_to='call_to_actions/', default='call_to_actions/None/default_staff.jpg')),
            ],
        ),
    ]
