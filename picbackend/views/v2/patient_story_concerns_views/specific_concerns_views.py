"""
This module defines views that handle hospital/provider locations for provider networks contracted with PIC
"""

from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..utils import clean_string_value_from_dict_object
from picmodels.models import ConsumerSpecificConcern
from ..utils import add_specific_concern_using_api_rqst_params
from ..utils import modify_specific_concern_using_api_rqst_params
from ..utils import modify_specific_concern_add_general_concern_using_api_rqst_params
from ..utils import modify_specific_concern_remove_general_concern_using_api_rqst_params
from ..utils import delete_specific_concern_using_api_rqst_params
from ..base import JSONPUTRspMixin
from ..base import JSONGETRspMixin


#Need to abstract common variables in get and post class methods into class attributes
class SpecificConcernsManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles healthcare carrier related requests
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SpecificConcernsManagementView, self).dispatch(request, *args, **kwargs)

    def specific_concerns_management_put_logic(self, post_data, response_raw_data, post_errors):
        # Retrieve database action from post data
        rqst_action = clean_string_value_from_dict_object(post_data, "root", "Database Action", post_errors)

        # If there are no parsing errors, process PUT data based on database action
        if not post_errors:
            if rqst_action == "Add Specific Concern":
                response_raw_data = add_specific_concern_using_api_rqst_params(response_raw_data, post_data, post_errors)
            elif rqst_action == "Modify Specific Concern":
                response_raw_data = modify_specific_concern_using_api_rqst_params(response_raw_data, post_data, post_errors)
            elif rqst_action == "Modify Specific Concern - add_general_concern":
                response_raw_data = modify_specific_concern_add_general_concern_using_api_rqst_params(response_raw_data, post_data, post_errors)
            elif rqst_action == "Modify Specific Concern - remove_general_concern":
                response_raw_data = modify_specific_concern_remove_general_concern_using_api_rqst_params(response_raw_data, post_data, post_errors)
            elif rqst_action == "Delete Specific Concern":
                response_raw_data = delete_specific_concern_using_api_rqst_params(response_raw_data, post_data, post_errors)

        return response_raw_data, post_errors

    def specific_concerns_management_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        specific_concerns = ConsumerSpecificConcern.objects.all()

        # if 'id' in search_params:
        #     rqst_provider_location_id = search_params['id']
        #     if rqst_provider_location_id != 'all':
        #         list_of_ids = search_params['id list']
        #     else:
        #         list_of_ids = None
        #     response_raw_data, rqst_errors = retrieve_provider_locations_by_id(response_raw_data, rqst_errors, provider_locations,
        #                                                                        rqst_provider_location_id, list_of_ids)
        # elif 'name' in search_params:
        #     rqst_name = search_params['name']
        #
        #     response_raw_data, rqst_errors = retrieve_provider_locations_by_name(response_raw_data, rqst_errors,
        #                                                                          provider_locations, rqst_name)
        # elif 'network_name' in search_params:
        #     rqst_network_name = search_params['network_name']
        #
        #     response_raw_data, rqst_errors = retrieve_provider_locations_by_network_name(response_raw_data, rqst_errors,
        #                                                                                  provider_locations, rqst_network_name)
        # elif 'network_id' in search_params:
        #     rqst_network_id = search_params['network_id']
        #     list_of_network_ids = search_params['network_id_list']
        #
        #     response_raw_data, rqst_errors = retrieve_provider_locations_by_network_id(response_raw_data, rqst_errors,
        #                                                                                provider_locations, rqst_network_id,
        #                                                                                list_of_network_ids)

        return response_raw_data, rqst_errors

    put_logic_function = specific_concerns_management_put_logic
    get_logic_function = specific_concerns_management_get_logic