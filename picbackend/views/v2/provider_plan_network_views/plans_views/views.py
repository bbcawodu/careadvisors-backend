"""
This module defines views that handle accepted plans for provider networks contracted with PIC
"""

from django.views.generic import View
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


# Need to abstract common variables in get and post class methods into class attributes
class PlansManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    def plans_management_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        rqst_action = clean_string_value_from_dict_object(rqst_body, "root", "Database Action", rqst_errors)

        if not rqst_errors:
            healthcare_plan_instance = None

            if rqst_action == "Plan Addition":
                healthcare_plan_instance = validate_rqst_params_and_add_instance(rqst_body, rqst_errors)
            elif rqst_action == "Plan Modification":
                healthcare_plan_instance = validate_rqst_params_and_modify_instance(rqst_body, rqst_errors)
            elif rqst_action == "Plan Deletion":
                validate_rqst_params_and_delete_instance(rqst_body, rqst_errors)

                if not rqst_errors:
                    response_raw_data['Data']["Database ID"] = "Deleted"
            else:
                rqst_errors.append("No valid 'Database Action' provided.")

            if healthcare_plan_instance:
                response_raw_data['Data']["Database ID"] = healthcare_plan_instance.id

    def plans_management_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        def retrieve_data_by_primary_params_and_add_to_response():
            data_list = None

            if 'id' in validated_GET_rqst_params:
                rqst_plan_id = validated_GET_rqst_params['id']
                if rqst_plan_id != 'all':
                    list_of_ids = validated_GET_rqst_params['id_list']
                else:
                    list_of_ids = None

                data_list = retrieve_plan_data_by_id(validated_GET_rqst_params, rqst_plan_id, list_of_ids, rqst_errors)
            elif 'name' in validated_GET_rqst_params:
                rqst_name = validated_GET_rqst_params['name']

                data_list = retrieve_plan_data_by_name(validated_GET_rqst_params, rqst_name, rqst_errors)
            elif 'carrier_state' in validated_GET_rqst_params:
                list_of_carrier_states = validated_GET_rqst_params['carrier_state_list']

                data_list = retrieve_plan_data_by_carrier_state(validated_GET_rqst_params, list_of_carrier_states, rqst_errors)
            elif 'carrier_name' in validated_GET_rqst_params:
                rqst_carrier_name = validated_GET_rqst_params['carrier_name']

                data_list = retrieve_plan_data_by_carrier_name(validated_GET_rqst_params, rqst_carrier_name, rqst_errors)
            elif 'carrier_id' in validated_GET_rqst_params:
                list_of_carrier_ids = validated_GET_rqst_params['carrier_id_list']

                data_list = retrieve_plan_data_by_carrier_id(validated_GET_rqst_params, list_of_carrier_ids, rqst_errors)
            elif 'accepted_location_id' in validated_GET_rqst_params:
                list_of_accepted_location_ids = validated_GET_rqst_params['accepted_location_id_list']

                data_list = retrieve_plan_data_by_accepted_location_id(validated_GET_rqst_params, list_of_accepted_location_ids, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response()

    parse_PUT_request_and_add_response = plans_management_put_logic

    accepted_GET_request_parameters = [
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
    parse_GET_request_and_add_response = plans_management_get_logic
