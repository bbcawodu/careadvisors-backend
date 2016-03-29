# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0019_metricssubmission_coverage_stats'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plan_name', models.CharField(default=b'Miscellaneous', max_length=1000, choices=[(b'Blue Cross Blue Shield', b'Blue Cross Blue Shield'), (b'Harken Health', b'Harken Health'), (b'Land of Lincoln', b'Land of Lincoln'), (b'Miscellaneous', b'Miscellaneous')])),
                ('enrollments', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='metricssubmission',
            name='coverage_stats',
        ),
        migrations.AddField(
            model_name='metricssubmission',
            name='plan_stats',
            field=models.ManyToManyField(to='picmodels.PlanStat'),
        ),
    ]
