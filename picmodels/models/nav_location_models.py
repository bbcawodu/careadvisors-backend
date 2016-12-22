"""
This file defines the data models for the picproject app
"""

from django.db import models
from picmodels.models import Address


class NavMetricsLocation(models.Model):
    """Model to store addresses for accounts"""
    name = models.CharField(max_length=200, unique=True)
    address = models.ForeignKey(Address, blank=True, null=True)

    class Meta:
        app_label = 'picmodels'
        verbose_name_plural = "Navigator Metrics Locations"
        unique_together = ("address",)

    def return_values_dict(self):
        valuesdict = {"Name": self.name,
                      "Database ID": self.id,
                      }

        if self.address:
            address_values = self.address.return_values_dict()
            for key in address_values:
                valuesdict[key] = address_values[key]
        return valuesdict
