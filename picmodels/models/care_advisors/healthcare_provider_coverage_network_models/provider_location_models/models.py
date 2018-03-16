from django.db import models
import urllib

from picmodels.models.care_advisors.healthcare_provider_coverage_network_models import HealthcarePlan
from picmodels.models.care_advisors.healthcare_provider_coverage_network_models import ProviderNetwork

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params
from .services.create_update_delete import check_for_provider_location_objs_with_given_name_and_network

from .services.read import get_serialized_rows_by_id
from .services.read import get_serialized_rows_by_name
from .services.read import get_serialized_rows_by_network_id
from .services.read import get_serialized_rows_by_network_name

class ProviderLocation(models.Model):
    name = models.CharField(max_length=10000)
    accepted_plans = models.ManyToManyField(
        HealthcarePlan,
        blank=True,
        related_name='locations_accepted_at'
    )
    provider_network = models.ForeignKey(
        ProviderNetwork,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def return_values_dict(self):
        valuesdict = {"name": self.name,
                      "url_encoded_name": urllib.parse.quote(self.name) if self.name else None,
                      "provider_network info": None,
                      "accepted_plans": None,
                      "Database ID": self.id}

        if self.provider_network:
            provider_network_object = self.provider_network
            provider_network_info = {
                                        "name": provider_network_object.name,
                                        "Database ID": provider_network_object.id
                                    }
            valuesdict['provider_network info'] = provider_network_info

        accepted_plans_queryset = self.accepted_plans.all()
        if len(accepted_plans_queryset):
            accepted_plans_ids = []
            for plan_object in accepted_plans_queryset:
                accepted_plans_ids.append(plan_object.id)
            valuesdict['accepted_plans'] = accepted_plans_ids

        return valuesdict

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


ProviderLocation.create_row_w_validated_params = classmethod(create_row_w_validated_params)
ProviderLocation.update_row_w_validated_params = classmethod(update_row_w_validated_params)
ProviderLocation.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)
ProviderLocation.check_for_provider_location_objs_with_given_name_and_network = classmethod(check_for_provider_location_objs_with_given_name_and_network)

ProviderLocation.get_serialized_rows_by_id = classmethod(get_serialized_rows_by_id)
ProviderLocation.get_serialized_rows_by_name = classmethod(get_serialized_rows_by_name)
ProviderLocation.get_serialized_rows_by_network_id = classmethod(get_serialized_rows_by_network_id)
ProviderLocation.get_serialized_rows_by_network_name = classmethod(get_serialized_rows_by_network_name)
