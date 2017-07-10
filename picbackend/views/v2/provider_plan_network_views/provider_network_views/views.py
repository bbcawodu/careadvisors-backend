"""
This module defines views that handle CRUD for provider networks contracted with PIC
"""

from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from picmodels.models import ProviderNetwork
from ...utils import clean_string_value_from_dict_object
from ...utils import JSONPUTRspMixin
from ...utils import JSONGETRspMixin
from .tools import validate_rqst_params_and_add_instance
from .tools import validate_rqst_params_and_modify_instance
from .tools import validate_rqst_params_and_delete_instance
from .tools import retrieve_provider_network_data_by_id
from .tools import retrieve_provider_network_data_by_name


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
            provider_network_obj = None

            if rqst_action == "Provider Network Addition":
                provider_network_obj = validate_rqst_params_and_add_instance(post_data, post_errors)
            elif rqst_action == "Provider Network Modification":
                provider_network_obj = validate_rqst_params_and_modify_instance(post_data, post_errors)
            elif rqst_action == "Provider Network Deletion":
                validate_rqst_params_and_delete_instance(post_data, post_errors)

                if not post_errors:
                    response_raw_data['Data']["Database ID"] = "Deleted"
            else:
                post_errors.append("No valid 'Database Action' provided.")

            if provider_network_obj:
                response_raw_data['Data']["Database ID"] = provider_network_obj.id

    def provider_networks_management_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        provider_networks = ProviderNetwork.objects.all()

        def retrieve_data_by_primary_params_and_add_to_response(db_objects):
            data_list = []

            if 'id' in search_params:
                rqst_provider_network_id = search_params['id']
                if rqst_provider_network_id != 'all':
                    list_of_ids = search_params['id list']
                else:
                    list_of_ids = None

                data_list = retrieve_provider_network_data_by_id(db_objects, rqst_provider_network_id, list_of_ids, rqst_errors)
            elif 'name' in search_params:
                rqst_name = search_params['name']

                data_list = retrieve_provider_network_data_by_name(db_objects, rqst_name, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response(provider_networks)

    put_logic_function = provider_networks_management_put_logic

    accepted_get_parameters = [
        "id",
        "name"
    ]
    get_logic_function = provider_networks_management_get_logic
