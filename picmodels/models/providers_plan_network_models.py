"""
This module defines the db Tables for storing provider networks and the plans that they accept.
"""

from django.db import models


class HealthcareCarrier(models.Model):
    name = models.CharField(max_length=10000)

    def return_values_dict(self):
        valuesdict = {"name": self.name,
                      "Database ID": self.id}

        # add related plans to values dict
        member_plans = []
        for plan_object in self.healthcareplan_set.all():
            member_plans.append(plan_object.return_values_dict())
        if member_plans:
            valuesdict["plans"] = member_plans

        return valuesdict


class HealthcarePlan(models.Model):
    name = models.CharField(max_length=10000)
    carrier = models.ForeignKey(HealthcareCarrier, on_delete=models.CASCADE, blank=True, null=True)

    def return_values_dict(self):
        valuesdict = {"name": self.name,
                      "Database ID": self.id}

        return valuesdict


class ProviderNetwork(models.Model):
    name = models.CharField(max_length=10000)

    def return_values_dict(self):
        valuesdict = {"name": self.name,
                      "Database ID": self.id}

        return valuesdict


class ProviderLocation(models.Model):
    name = models.CharField(max_length=10000)
    accepted_plans = models.ManyToManyField(HealthcarePlan, blank=True)
    provider_network = models.ForeignKey(ProviderNetwork, on_delete=models.CASCADE, blank=True, null=True)

    def return_values_dict(self):
        valuesdict = {"name": self.name,
                      "Database ID": self.id}

        return valuesdict
