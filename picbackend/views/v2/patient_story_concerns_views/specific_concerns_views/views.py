"""
This module defines views that handle hospital/provider locations for provider networks contracted with PIC
"""

from django.views.generic import View

from picbackend.views.utils import JSONGETRspMixin
from picbackend.views.utils import JSONPUTRspMixin

from picmodels.models import ConsumerSpecificConcern

from .tools import validate_put_rqst_params


class SpecificConcernsManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    def specific_concerns_management_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        validated_put_rqst_params = validate_put_rqst_params(rqst_body, rqst_errors)
        rqst_action = validated_put_rqst_params['rqst_action']

        # If there are no parsing errors, process PUT data based on database action
        if not rqst_errors:
            specific_concern_row = None

            if rqst_action == "create":
                specific_concern_row = ConsumerSpecificConcern.create_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors)

            elif rqst_action == "update":
                specific_concern_row = ConsumerSpecificConcern.update_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )
            elif rqst_action == "delete":
                ConsumerSpecificConcern.delete_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )

                if not rqst_errors:
                    response_raw_data['Data']["row"] = "Deleted"
            else:
                rqst_errors.append("No valid 'db_action' provided.")

            if specific_concern_row:
                response_raw_data['Data']["row"] = specific_concern_row.return_values_dict()

    def specific_concerns_management_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        def retrieve_data_by_primary_params_and_add_to_response():
            data_list = []

            if 'id' in validated_GET_rqst_params:
                rqst_specific_concern_id = validated_GET_rqst_params['id']
                if rqst_specific_concern_id != 'all':
                    list_of_ids = validated_GET_rqst_params['id_list']
                else:
                    list_of_ids = None

                data_list = ConsumerSpecificConcern.retrieve_specific_concern_data_by_id(
                    rqst_specific_concern_id,
                    list_of_ids,
                    rqst_errors
                )
            elif 'question' in validated_GET_rqst_params:
                rqst_question = validated_GET_rqst_params['question']

                data_list = ConsumerSpecificConcern.retrieve_specific_concern_data_by_question(
                    rqst_question,
                    rqst_errors
                )
            elif 'gen_concern_name' in validated_GET_rqst_params:
                rqst_gen_concern_name = validated_GET_rqst_params['gen_concern_name']

                data_list = ConsumerSpecificConcern.retrieve_specific_concern_data_by_gen_concern_name(
                    rqst_gen_concern_name,
                    rqst_errors
                )
            elif 'gen_concern_id_subset' in validated_GET_rqst_params:
                list_of_gen_concern_ids = validated_GET_rqst_params['gen_concern_id_subset_list']

                data_list = ConsumerSpecificConcern.retrieve_specific_concern_data_by_gen_concern_id_subset(
                    list_of_gen_concern_ids,
                    rqst_errors
                )
            elif 'gen_concern_id' in validated_GET_rqst_params:
                list_of_gen_concern_ids = validated_GET_rqst_params['gen_concern_id_list']

                data_list = ConsumerSpecificConcern.retrieve_specific_concern_data_by_gen_concern_id(
                    list_of_gen_concern_ids,
                    rqst_errors
                )
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response()

    parse_PUT_request_and_add_response = specific_concerns_management_put_logic

    accepted_GET_request_parameters = [
        "id",
        "question",
        "gen_concern_name",
        "gen_concern_id_subset",
        "gen_concern_id"
    ]
    parse_GET_request_and_add_response = specific_concerns_management_get_logic
