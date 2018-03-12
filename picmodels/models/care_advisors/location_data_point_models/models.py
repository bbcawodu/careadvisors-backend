from django.db import models
from picmodels.models.care_advisors import Address

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params

from .services.read import retrieve_nav_hub_location_data_by_id


class NavMetricsLocation(models.Model):
    """Model to store addresses for accounts"""
    name = models.CharField(max_length=200, unique=True)
    address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.SET_NULL)

    cps_location = models.BooleanField(default=False)

    class Meta:
        app_label = 'picmodels'
        verbose_name_plural = "Navigator Metrics Locations"
        unique_together = ("address", "name")

    def return_values_dict(self):
        valuesdict = {
            "Name": self.name,
            "Database ID": self.id,
            "CPS Location": self.cps_location,
        }

        if self.address:
            address_values = self.address.return_values_dict()
            for key in address_values:
                if key != "id":
                    valuesdict[key] = address_values[key]
        return valuesdict


NavMetricsLocation.create_row_w_validated_params = classmethod(create_row_w_validated_params)
NavMetricsLocation.update_row_w_validated_params = classmethod(update_row_w_validated_params)
NavMetricsLocation.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)

NavMetricsLocation.retrieve_nav_hub_location_data_by_id = classmethod(retrieve_nav_hub_location_data_by_id)
