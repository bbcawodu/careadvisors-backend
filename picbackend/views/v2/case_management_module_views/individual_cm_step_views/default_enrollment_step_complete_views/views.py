from django.views.generic import View

from picbackend.views.utils import JSONGETRspMixin
from picbackend.views.utils import JSONPUTRspMixin

from picmodels.models import DefaultEnrollmentStepComplete

from .tools import validate_put_rqst_params


# Need to abstract common variables in get and post class methods into class attributes
class DefaultEnrollmentStepCompleteManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    def default_enrollment_step_complete_management_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        validated_put_rqst_params = validate_put_rqst_params(rqst_body, rqst_errors)
        rqst_action = validated_put_rqst_params['rqst_action']

        if not rqst_errors:
            if rqst_action == "create":
                row = DefaultEnrollmentStepComplete.create_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )

                if row:
                    response_raw_data['Data']["row"] = row.return_values_dict()
            elif rqst_action == "update":
                row = DefaultEnrollmentStepComplete.update_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )

                if row:
                    response_raw_data['Data']["row"] = row.return_values_dict()
            elif rqst_action == "delete":
                DefaultEnrollmentStepComplete.delete_row_w_validated_params(validated_put_rqst_params, rqst_errors)

                if not rqst_errors:
                    response_raw_data['Data']["row"] = "Deleted"
            else:
                rqst_errors.append("No valid 'db_action' provided.")

    def default_enrollment_step_complete_management_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        def retrieve_data_and_add_to_response():
            if 'id' in validated_GET_rqst_params:
                data_list = DefaultEnrollmentStepComplete.get_serialized_rows_by_id(validated_GET_rqst_params, rqst_errors)
            else:
                data_list = []
                rqst_errors.append('No Valid Parameters')

            response_raw_data["Data"] = data_list

        retrieve_data_and_add_to_response()

    parse_PUT_request_and_add_response = default_enrollment_step_complete_management_put_logic

    accepted_GET_request_parameters = [
        "id",
        "consumer_id",
        "nav_id",
        "cm_client_id",
        'cm_sequence_id',
        "date_created_start",
        "date_created_end",
        "date_modified_start",
        "date_modified_end",
        "datetime_completed_start_date",
        "datetime_completed_end_date",
    ]
    parse_GET_request_and_add_response = default_enrollment_step_complete_management_get_logic
