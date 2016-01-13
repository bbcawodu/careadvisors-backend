# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0008_auto_20151222_1552'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetricsSubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('received_education', models.IntegerField()),
                ('applied_medicaid', models.IntegerField()),
                ('selected_qhp', models.IntegerField()),
                ('enrolled_shop', models.IntegerField()),
                ('ref_medicaid_or_chip', models.IntegerField()),
                ('ref_shop', models.IntegerField()),
                ('filed_exemptions', models.IntegerField()),
                ('rec_postenroll_support', models.IntegerField()),
                ('trends', models.CharField(max_length=5000)),
                ('success_story', models.CharField(max_length=5000)),
                ('hardship_or_difficulty', models.CharField(max_length=5000)),
                ('comments', models.CharField(max_length=5000, null=True, blank=True)),
                ('outreach_stakeholder_activity', models.CharField(max_length=5000, null=True, blank=True)),
                ('appointments_scheduled', models.IntegerField(null=True)),
                ('confirmation_calls', models.IntegerField(null=True)),
                ('appointments_held', models.IntegerField(null=True)),
                ('appointments_over_hour', models.IntegerField(null=True)),
                ('appointments_cmplx_market', models.IntegerField(null=True)),
                ('appointments_cmplx_medicaid', models.IntegerField(null=True)),
                ('appointments_postenroll_assistance', models.IntegerField(null=True)),
                ('appointments_over_three_hours', models.IntegerField(null=True)),
                ('staff_member', models.ForeignKey(to='picmodels.PICStaff')),
            ],
        ),
    ]
