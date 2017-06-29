"""
This module defines views that handle hospital/provider locations for provider networks contracted with PIC
"""

from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from picmodels.models import ProviderLocation
from ...utils import clean_string_value_from_dict_object
from ...base import JSONPUTRspMixin
from ...base import JSONGETRspMixin
from .tools import validate_rqst_params_and_add_instance
from .tools import validate_rqst_params_and_modify_instance
from .tools import validate_rqst_params_and_add_accepted_plans_to_instance
from .tools import validate_rqst_params_and_remove_accepted_plans_from_instance
from .tools import validate_rqst_params_and_delete_instance
from .tools import retrieve_provider_locations_by_id
from .tools import retrieve_provider_locations_by_name
from .tools import retrieve_provider_locations_by_network_name
from .tools import retrieve_provider_locations_by_network_id


#Need to abstract common variables in get and post class methods into class attributes
class ProviderLocationsManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles healthcare carrier related requests
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ProviderLocationsManagementView, self).dispatch(request, *args, **kwargs)

    def provider_locations_management_put_logic(self, post_data, response_raw_data, post_errors):
        rqst_action = clean_string_value_from_dict_object(post_data, "root", "Database Action", post_errors)

        if not post_errors:
            provider_location_obj = None

            if rqst_action == "Add Provider Location":
                provider_location_obj = validate_rqst_params_and_add_instance(post_data, post_errors)
            elif rqst_action == "Modify Provider Location":
                provider_location_obj = validate_rqst_params_and_modify_instance(post_data, post_errors)
            elif rqst_action == "Modify Provider Location - add_accepted_plans":
                provider_location_obj = validate_rqst_params_and_add_accepted_plans_to_instance(post_data, post_errors)
            elif rqst_action == "Modify Provider Location - remove_accepted_plans":
                provider_location_obj = validate_rqst_params_and_remove_accepted_plans_from_instance(post_data, post_errors)
            elif rqst_action == "Delete Provider Location":
                validate_rqst_params_and_delete_instance(post_data, post_errors)

                if not post_errors:
                    response_raw_data['Data']["Database ID"] = "Deleted"
            else:
                post_errors.append("No valid 'Database Action' provided.")

            if provider_location_obj:
                response_raw_data['Data']["Database ID"] = provider_location_obj.id

    def provider_locations_management_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        provider_locations = ProviderLocation.objects.all()

        def retrieve_data_by_primary_params_and_add_to_response(db_objects):
            data_list = []

            if 'id' in search_params:
                rqst_provider_location_id = search_params['id']
                if rqst_provider_location_id != 'all':
                    list_of_ids = search_params['id list']
                else:
                    list_of_ids = None

                data_list = retrieve_provider_locations_by_id(db_objects, rqst_provider_location_id, list_of_ids, rqst_errors)
            elif 'name' in search_params:
                rqst_name = search_params['name']

                data_list = retrieve_provider_locations_by_name(db_objects, rqst_name, rqst_errors)
            elif 'network_name' in search_params:
                rqst_network_name = search_params['network_name']

                data_list = retrieve_provider_locations_by_network_name(db_objects, rqst_network_name, rqst_errors)
            elif 'network_id' in search_params:
                list_of_network_ids = search_params['network_id_list']

                data_list = retrieve_provider_locations_by_network_id(db_objects, list_of_network_ids, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response(provider_locations)

    put_logic_function = provider_locations_management_put_logic
    get_logic_function = provider_locations_management_get_logic
