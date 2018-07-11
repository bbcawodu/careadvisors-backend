# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0087_defaultenrollmentstep2'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultEnrollmentStepComplete',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('datetime_completed', models.DateTimeField(blank=True, null=True)),
                ('client_appointment_datetime', models.DateTimeField(blank=True, null=True)),
                ('date_created', models.DateTimeField(null=True, auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('cm_client', models.ForeignKey(to='picmodels.CaseManagementClient')),
                ('cm_sequence', models.ForeignKey(to='picmodels.CMSequences')),
                ('consumer', models.ForeignKey(to='picmodels.PICConsumer')),
                ('navigator', models.ForeignKey(to='picmodels.Navigators')),
            ],
            options={
                'rest_url': 'default_enrollment_step_complete',
            },
        ),
    ]
