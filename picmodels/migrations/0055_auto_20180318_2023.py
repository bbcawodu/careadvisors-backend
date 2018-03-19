# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0054_providerlocation_state_province'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('school', models.CharField(max_length=100)),
                ('major', models.CharField(max_length=100)),
                ('degree_type', models.CharField(null=True, blank=True, max_length=100, default='Not Available', choices=[('undergraduate', 'undergraduate'), ('graduate', 'graduate'), ('bachelors', 'bachelors'), ('masters', 'masters'), ('Not Available', 'Not Available')])),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('company', models.CharField(max_length=200)),
                ('description', models.TextField(null=True, blank=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('profile_description', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='picconsumer',
            name='healthcare_networks_used',
        ),
        migrations.RemoveField(
            model_name='picconsumerbackup',
            name='healthcare_networks_used',
        ),
        migrations.AddField(
            model_name='navigators',
            name='address',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, to='picmodels.Address'),
        ),
        migrations.AddField(
            model_name='navigators',
            name='healthcare_locations_worked',
            field=models.ManyToManyField(blank=True, to='picmodels.ProviderLocation', related_name='navigators_working_here'),
        ),
        migrations.AddField(
            model_name='navigators',
            name='healthcare_service_expertises',
            field=models.ManyToManyField(blank=True, to='picmodels.ProviderLocation', related_name='navigators_with_expertise'),
        ),
        migrations.AddField(
            model_name='navigators',
            name='insurance_carrier_specialties',
            field=models.ManyToManyField(blank=True, to='picmodels.HealthcareCarrier'),
        ),
        migrations.AddField(
            model_name='navigators',
            name='phone',
            field=models.CharField(null=True, blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='navigators',
            name='reported_region',
            field=models.CharField(null=True, blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='navigators',
            name='video_link',
            field=models.TextField(null=True, validators=[django.core.validators.URLValidator()], blank=True),
        ),
        migrations.AddField(
            model_name='picconsumer',
            name='healthcare_locations_used',
            field=models.ManyToManyField(blank=True, to='picmodels.ProviderLocation'),
        ),
        migrations.AddField(
            model_name='picconsumerbackup',
            name='healthcare_locations_used',
            field=models.ManyToManyField(blank=True, to='picmodels.ProviderLocation'),
        ),
        migrations.AddField(
            model_name='resume',
            name='navigator',
            field=models.ForeignKey(to='picmodels.Navigators'),
        ),
        migrations.AddField(
            model_name='job',
            name='Resume',
            field=models.ForeignKey(to='picmodels.Resume'),
        ),
        migrations.AddField(
            model_name='education',
            name='Resume',
            field=models.ForeignKey(to='picmodels.Resume'),
        ),
    ]
