"""
This module defines the db Tables for storing provider networks and the plans that they accept.
"""

from django.db import models


class HealthcareCarrier(models.Model):
    name = models.CharField(max_length=10000)


class HealthcarePlan(models.Model):
    name = models.CharField(max_length=10000)
    carrier = models.ForeignKey(HealthcareCarrier, on_delete=models.CASCADE, blank=True, null=True)


class ProviderNetwork(models.Model):
    name = models.CharField(max_length=10000)


class ProviderLocation(models.Model):
    name = models.CharField(max_length=10000)
    accepted_plans = models.ManyToManyField(HealthcarePlan, blank=True)
    provider_network = models.ForeignKey(ProviderNetwork, on_delete=models.CASCADE, blank=True, null=True)
