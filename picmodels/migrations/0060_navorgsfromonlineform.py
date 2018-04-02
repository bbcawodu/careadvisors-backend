# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0059_auto_20180330_1752'),
    ]

    operations = [
        migrations.CreateModel(
            name='NavOrgsFromOnlineForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('company_name', models.CharField(blank=True, max_length=1000, null=True)),
                ('estimated_monthly_caseload', models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(0)], null=True)),
                ('contact_first_name', models.CharField(blank=True, max_length=500, null=True)),
                ('contact_last_name', models.CharField(blank=True, max_length=500, null=True)),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('contact_phone', models.CharField(blank=True, max_length=500, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('appointment_datetime', models.DateTimeField(blank=True, null=True)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='picmodels.Address')),
            ],
        ),
    ]
