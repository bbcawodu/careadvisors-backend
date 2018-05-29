# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0072_navigators_approved_clients_for_case_management'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('outcome', models.CharField(max_length=5000, blank=True, null=True)),
                ('status', models.CharField(max_length=1000, blank=True, null=True, default='Not Available', choices=[('Voice Message', 'Voice Message'), ('Completed', 'Completed'), ('Not Available', 'Not Available')])),
                ('datetime_contacted', models.DateTimeField(blank=True, null=True)),
                ('contact_type', models.CharField(max_length=1000, blank=True, null=True, default='Not Available', choices=[('Email', 'Email'), ('Text', 'Text'), ('Phone', 'Phone'), ('In-Person', 'In-Person'), ('Not Available', 'Not Available')])),
                ('date_created', models.DateTimeField(null=True, auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('cm_client', models.ForeignKey(blank=True, null=True, to='picmodels.CaseManagementClient')),
            ],
        ),
        migrations.AddField(
            model_name='picconsumer',
            name='gender',
            field=models.CharField(max_length=1000, blank=True, null=True, default='Not Available', choices=[('Male', 'Male'), ('Female', 'Female'), ('Traansgender', 'Traansgender'), ('Not Available', 'Not Available')]),
        ),
        migrations.AddField(
            model_name='picconsumerbackup',
            name='gender',
            field=models.CharField(max_length=1000, blank=True, null=True, default='Not Available', choices=[('Male', 'Male'), ('Female', 'Female'), ('Traansgender', 'Traansgender'), ('Not Available', 'Not Available')]),
        ),
        migrations.AddField(
            model_name='contactlog',
            name='consumer',
            field=models.ForeignKey(to='picmodels.PICConsumer'),
        ),
        migrations.AddField(
            model_name='contactlog',
            name='navigator',
            field=models.ForeignKey(to='picmodels.Navigators'),
        ),
    ]
