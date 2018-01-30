"""
This file defines the data models for the picproject app
"""

from django.db import models


class Country(models.Model):
    """Model for countries"""
    name = models.CharField(max_length=45, blank=False)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'picmodels'
        verbose_name_plural = "Countries"
        ordering = ["name"]


class Address(models.Model):
    """Model to store addresses for accounts"""
    address_line_1 = models.CharField("Address line 1", max_length=45)
    address_line_2 = models.CharField("Address line 2", max_length=45, blank=True)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=50, blank=False)
    state_province = models.CharField("State/Province", max_length=40, blank=True)
    country = models.ForeignKey(Country, blank=False)

    class Meta:
        app_label = 'picmodels'
        unique_together = ("address_line_1", "address_line_2", "zipcode",
                           "city", "state_province", "country")

    def return_values_dict(self):
        valuesdict = {
            "address_line_1": self.address_line_1,
            "address_line_2": self.address_line_2,
            "zipcode": self.zipcode,
            "city": self.city,
            "state_province": self.state_province,
            "country": self.country.name,
            "id": self.id,
        }

        return valuesdict
