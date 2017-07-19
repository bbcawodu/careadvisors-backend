"""
This module defines views that handle accepted plans for provider networks contracted with PIC
"""

from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ...utils import clean_string_value_from_dict_object
from ...utils import JSONPUTRspMixin
from ...utils import JSONGETRspMixin
from .tools import validate_rqst_params_and_add_instance
from .tools import validate_rqst_params_and_modify_instance
from .tools import validate_rqst_params_and_delete_instance
from .tools import retrieve_plan_data_by_id
from .tools import retrieve_plan_data_by_name
from .tools import retrieve_plan_data_by_carrier_id
from .tools import retrieve_plan_data_by_carrier_state
from .tools import retrieve_plan_data_by_carrier_name
from .tools import retrieve_plan_data_by_accepted_location_id


#Need to abstract common variables in get and post class methods into class attributes
class PlansManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles healthcare carrier related requests
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PlansManagementView, self).dispatch(request, *args, **kwargs)

    def plans_management_put_logic(self, post_data, response_raw_data, post_errors):
        rqst_action = clean_string_value_from_dict_object(post_data, "root", "Database Action", post_errors)

        if not post_errors:
            healthcare_plan_instance = None

            if rqst_action == "Plan Addition":
                healthcare_plan_instance = validate_rqst_params_and_add_instance(post_data, post_errors)
            elif rqst_action == "Plan Modification":
                healthcare_plan_instance = validate_rqst_params_and_modify_instance(post_data, post_errors)
            elif rqst_action == "Plan Deletion":
                validate_rqst_params_and_delete_instance(post_data, post_errors)

                if not post_errors:
                    response_raw_data['Data']["Database ID"] = "Deleted"
            else:
                post_errors.append("No valid 'Database Action' provided.")

            if healthcare_plan_instance:
                response_raw_data['Data']["Database ID"] = healthcare_plan_instance.id

    def plans_management_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        def retrieve_data_by_primary_params_and_add_to_response():
            data_list = None

            if 'id' in search_params:
                rqst_plan_id = search_params['id']
                if rqst_plan_id != 'all':
                    list_of_ids = search_params['id_list']
                else:
                    list_of_ids = None

                data_list = retrieve_plan_data_by_id(search_params, rqst_plan_id, list_of_ids, rqst_errors)
            elif 'name' in search_params:
                rqst_name = search_params['name']

                data_list = retrieve_plan_data_by_name(search_params, rqst_name, rqst_errors)
            elif 'carrier state' in search_params:
                list_of_carrier_states = search_params['carrier state list']

                data_list = retrieve_plan_data_by_carrier_state(search_params, list_of_carrier_states, rqst_errors)
            elif 'carrier name' in search_params:
                rqst_carrier_name = search_params['carrier name']

                data_list = retrieve_plan_data_by_carrier_name(search_params, rqst_carrier_name, rqst_errors)
            elif 'carrier_id' in search_params:
                list_of_carrier_ids = search_params['carrier_id_list']

                data_list = retrieve_plan_data_by_carrier_id(search_params, list_of_carrier_ids, rqst_errors)
            elif 'accepted_location_id' in search_params:
                list_of_accepted_location_ids = search_params['accepted_location_id_list']

                data_list = retrieve_plan_data_by_accepted_location_id(search_params, list_of_accepted_location_ids, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response()

    put_logic_function = plans_management_put_logic

    accepted_get_parameters = [
        "id",
        "name",
        'carrier_state',
        'carrier_name',
        'carrier_id',
        'accepted_location_id',
        "include_summary_report",
        "include_detailed_report",
        "premium_type"
    ]
    get_logic_function = plans_management_get_logic
