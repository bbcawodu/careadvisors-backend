from django.views.generic import View

from picbackend.views.utils import JSONGETRspMixin
from picbackend.views.utils import JSONPUTRspMixin

from picmodels.models import StepsForCMSequences

from .tools import validate_put_rqst_params


# Need to abstract common variables in get and post class methods into class attributes
class StepsForCMSequencesManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles Patient Innovation Center navigator hub location instance related requests
    """

    def steps_for_cm_sequences_management_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        validated_put_rqst_params = validate_put_rqst_params(rqst_body, rqst_errors)
        rqst_action = validated_put_rqst_params['rqst_action']

        if not rqst_errors:
            if rqst_action == "create":
                row = StepsForCMSequences.create_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )

                if row:
                    response_raw_data['Data']["row"] = row.return_values_dict()
            elif rqst_action == "update":
                row = StepsForCMSequences.update_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )

                if row:
                    response_raw_data['Data']["row"] = row.return_values_dict()
            elif rqst_action == "delete":
                StepsForCMSequences.delete_row_w_validated_params(validated_put_rqst_params, rqst_errors)

                if not rqst_errors:
                    response_raw_data['Data']["row"] = "Deleted"
            else:
                rqst_errors.append("No valid 'db_action' provided.")

    def steps_for_cm_sequences_management_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        def retrieve_data_and_add_to_response():
            if 'id' in validated_GET_rqst_params:
                data_list = StepsForCMSequences.get_serialized_rows_by_id(validated_GET_rqst_params, rqst_errors)
            elif 'name' in validated_GET_rqst_params:
                data_list = StepsForCMSequences.get_serialized_rows_by_name(validated_GET_rqst_params, rqst_errors)
            else:
                data_list = []
                rqst_errors.append('No Valid Parameters')

            response_raw_data["Data"] = data_list

        retrieve_data_and_add_to_response()

    parse_PUT_request_and_add_response = steps_for_cm_sequences_management_put_logic

    accepted_GET_request_parameters = [
        "name",
        "id"
    ]
    parse_GET_request_and_add_response = steps_for_cm_sequences_management_get_logic
