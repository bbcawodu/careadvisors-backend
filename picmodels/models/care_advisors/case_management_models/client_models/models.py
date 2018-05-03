from django.db import models
from picmodels.models.care_advisors import Address

# from .services.create_update_delete import create_row_w_validated_params
# from .services.create_update_delete import update_row_w_validated_params
# from .services.create_update_delete import delete_row_w_validated_params
#
# from .services.read import retrieve_nav_hub_location_data_by_id


class CaseManagementClient(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        app_label = 'picmodels'
        verbose_name_plural = "Navigator Metrics Locations"
        unique_together = ("address", "name")

    def return_values_dict(self):
        values_dict = {
            "name": self.name,
            "id": self.id,
            "address": None
        }

        if self.address:
            address_values = self.address.return_values_dict()
            values_dict['address'] = address_values

        return values_dict


# CaseManagementClient.create_row_w_validated_params = classmethod(create_row_w_validated_params)
# CaseManagementClient.update_row_w_validated_params = classmethod(update_row_w_validated_params)
# CaseManagementClient.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)
#
# CaseManagementClient.retrieve_nav_hub_location_data_by_id = classmethod(retrieve_nav_hub_location_data_by_id)