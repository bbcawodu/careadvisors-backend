# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0004_auto_20151217_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.CharField(max_length=2000)),
                ('start_time', models.CharField(max_length=1000)),
                ('end_time', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1000)),
                ('address', models.CharField(max_length=2000)),
                ('location_phone', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='PICConsumer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=1000)),
                ('last_name', models.CharField(default=b'', max_length=1000)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=1000)),
                ('preferred_language', models.CharField(max_length=1000)),
                ('best_contact_time', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='PICStaff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=1000)),
                ('last_name', models.CharField(default=b'', max_length=1000)),
                ('email', models.EmailField(max_length=254)),
                ('type', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='picconsumer',
            unique_together=set([('first_name', 'last_name', 'email', 'phone', 'preferred_language', 'best_contact_time')]),
        ),
        migrations.AddField(
            model_name='appointment',
            name='consumer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='picmodels.PICConsumer', null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='picmodels.Location', null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='poc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='picmodels.PICStaff', null=True),
        ),
        migrations.AddField(
            model_name='picappointment',
            name='consumer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='picmodels.PICConsumer', null=True),
        ),
        migrations.AddField(
            model_name='picappointment',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='picmodels.Location', null=True),
        ),
        migrations.AddField(
            model_name='picappointment',
            name='poc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='picmodels.PICStaff', null=True),
        ),
    ]
