from django.db import models
from picmodels.models.care_advisors import Address

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params
from .services.create_update_delete import check_for_rows_with_given_name_and_address

from .services.read import get_serialized_rows_by_id
from .services.read import get_serialized_rows_by_name


class CaseManagementClient(models.Model):
    name = models.CharField(max_length=200)
    address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        app_label = 'picmodels'
        verbose_name_plural = "Case Management Clients"

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


CaseManagementClient.create_row_w_validated_params = classmethod(create_row_w_validated_params)
CaseManagementClient.update_row_w_validated_params = classmethod(update_row_w_validated_params)
CaseManagementClient.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)
CaseManagementClient.check_for_rows_with_given_name_and_address = classmethod(check_for_rows_with_given_name_and_address)
#
CaseManagementClient.get_serialized_rows_by_id = classmethod(get_serialized_rows_by_id)
CaseManagementClient.get_serialized_rows_by_name = classmethod(get_serialized_rows_by_name)