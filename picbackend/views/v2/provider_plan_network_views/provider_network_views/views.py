"""
This module defines views that handle CRUD for provider networks contracted with PIC
"""

from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from picmodels.models import ProviderNetwork
from ...utils import clean_string_value_from_dict_object
from ...base import JSONPUTRspMixin
from ...base import JSONGETRspMixin
from .tools import add_provider_network
from .tools import modify_provider_network
from .tools import delete_provider_network
from .tools import retrieve_provider_networks_by_id
from .tools import retrieve_provider_networks_by_name


#Need to abstract common variables in get and post class methods into class attributes
class ProviderNetworksManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles healthcare carrier related requests
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ProviderNetworksManagementView, self).dispatch(request, *args, **kwargs)

    def provider_networks_management_put_logic(self, post_data, response_raw_data, post_errors):
        # Retrieve database action from post data
        rqst_action = clean_string_value_from_dict_object(post_data, "root", "Database Action", post_errors)

        # If there are no parsing errors, process PUT data based on database action
        if not post_errors:
            if rqst_action == "Provider Network Addition":
                add_provider_network(response_raw_data, post_data, post_errors)
            elif rqst_action == "Provider Network Modification":
                modify_provider_network(response_raw_data, post_data, post_errors)
            elif rqst_action == "Provider Network Deletion":
                delete_provider_network(response_raw_data, post_data, post_errors)
            else:
                post_errors.append("No valid 'Database Action' provided.")

    def provider_networks_management_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        provider_networks = ProviderNetwork.objects.all()

        if 'id' in search_params:
            rqst_provider_network_id = search_params['id']
            if rqst_provider_network_id != 'all':
                list_of_ids = search_params['id list']
            else:
                list_of_ids = None
            retrieve_provider_networks_by_id(response_raw_data, rqst_errors, provider_networks, rqst_provider_network_id, list_of_ids)
        elif 'name' in search_params:
            rqst_name = search_params['name']

            retrieve_provider_networks_by_name(response_raw_data, rqst_errors, provider_networks, rqst_name)
        else:
            rqst_errors.append('No Valid Parameters')

    put_logic_function = provider_networks_management_put_logic
    get_logic_function = provider_networks_management_get_logic
