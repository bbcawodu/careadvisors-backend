"""
This module defines views that handle general concerns requests for the Navigator Online Plus patient story conversation
flow
"""

from django.views.generic import View

from picbackend.views.utils import JSONGETRspMixin
from picbackend.views.utils import JSONPUTRspMixin

from picmodels.models import ConsumerGeneralConcern

from .tools import validate_put_rqst_params


#Need to abstract common variables in get and post class methods into class attributes
class GeneralConcernsManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles healthcare carrier related requests
    """

    def general_concerns_management_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        validated_put_rqst_params = validate_put_rqst_params(rqst_body, rqst_errors)
        rqst_action = validated_put_rqst_params['rqst_action']

        # If there are no parsing errors, process PUT data based on database action
        if not rqst_errors:
            if rqst_action == "create":
                general_concern_obj = ConsumerGeneralConcern.create_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )

                if general_concern_obj:
                    response_raw_data['Data']["row"] = general_concern_obj.return_values_dict()
            elif rqst_action == "update":
                general_concern_obj = ConsumerGeneralConcern.update_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )

                if general_concern_obj:
                    response_raw_data['Data']["row"] = general_concern_obj.return_values_dict()
            elif rqst_action == "delete":
                ConsumerGeneralConcern.delete_row_w_validated_params(validated_put_rqst_params, rqst_errors)

                if not rqst_errors:
                    response_raw_data['Data']["row"] = "Deleted"
            else:
                rqst_errors.append("No valid 'db_action' provided.")

    def general_concerns_management_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        def retrieve_data_by_primary_params_and_add_to_response():
            data_list = []

            if 'id' in validated_GET_rqst_params:
                rqst_general_concerns_id = validated_GET_rqst_params['id']
                if rqst_general_concerns_id != 'all':
                    list_of_ids = validated_GET_rqst_params['id_list']
                else:
                    list_of_ids = None

                data_list = ConsumerGeneralConcern.retrieve_general_concerns_by_id(
                    rqst_general_concerns_id,
                    list_of_ids,
                    rqst_errors
                )
            elif 'name' in validated_GET_rqst_params:
                rqst_name = validated_GET_rqst_params['name']

                data_list = ConsumerGeneralConcern.retrieve_general_concerns_by_name(rqst_name, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response()

    parse_PUT_request_and_add_response = general_concerns_management_put_logic

    accepted_GET_request_parameters = [
        "id",
        "name"
    ]
    parse_GET_request_and_add_response = general_concerns_management_get_logic
