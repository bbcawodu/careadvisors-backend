from django.db import models
import urllib

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params
from .services.create_update_delete import check_for_provider_network_objs_with_given_name

from .services.read import get_serialized_rows_by_id
from .services.read import get_serialized_rows_by_name


class ProviderNetwork(models.Model):
    name = models.CharField(max_length=10000)

    def return_values_dict(self):
        valuesdict = {
            "name": self.name,
            "url_encoded_name": urllib.parse.quote(self.name) if self.name else None,
            "provider_locations": None,
            "Database ID": self.id
        }

        # add related plans to values dict
        provider_locations = []
        provider_location_qset = self.providerlocation_set.all()
        if len(provider_location_qset):
            for provider_location in provider_location_qset:
                provider_locations.append(provider_location.id)

        if provider_locations:
            valuesdict["provider_locations"] = provider_locations

        return valuesdict

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


ProviderNetwork.create_row_w_validated_params = classmethod(create_row_w_validated_params)
ProviderNetwork.update_row_w_validated_params = classmethod(update_row_w_validated_params)
ProviderNetwork.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)
ProviderNetwork.check_for_provider_network_objs_with_given_name = classmethod(check_for_provider_network_objs_with_given_name)

ProviderNetwork.get_serialized_rows_by_id = classmethod(get_serialized_rows_by_id)
ProviderNetwork.get_serialized_rows_by_name = classmethod(get_serialized_rows_by_name)
