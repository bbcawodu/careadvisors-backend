from django.views.generic import View

from picbackend.views.utils import JSONGETRspMixin
from picbackend.views.utils import JSONPUTRspMixin

from picmodels.models import HealthcareServiceExpertise

from .tools import validate_put_rqst_params


#Need to abstract common variables in get and post class methods into class attributes
class ServiceExpertiseManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    def create_update_delete_method_logic(self, rqst_body, response_raw_data, rqst_errors):
        validated_params = validate_put_rqst_params(rqst_body, rqst_errors)
        rqst_action = validated_params['rqst_action']

        if not rqst_errors:
            if rqst_action == "create":
                db_row = HealthcareServiceExpertise.create_row_w_validated_params(
                    validated_params,
                    rqst_errors
                )

                if db_row:
                    response_raw_data['Data']["row"] = db_row.return_values_dict()
            elif rqst_action == "update":
                db_row = HealthcareServiceExpertise.update_row_w_validated_params(
                    validated_params,
                    rqst_errors
                )

                if db_row:
                    response_raw_data['Data']["row"] = db_row.return_values_dict()
            elif rqst_action == "delete":
                HealthcareServiceExpertise.delete_row_w_validated_params(validated_params, rqst_errors)

                if not rqst_errors:
                    response_raw_data['Data']["row"] = "Deleted"
            else:
                rqst_errors.append("No valid 'db_action' provided.")

    def read_method_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        def retrieve_data_by_primary_params_and_add_to_response():
            data_list = []

            if 'id' in validated_GET_rqst_params:
                rqst_id = validated_GET_rqst_params['id']
                if rqst_id != 'all':
                    list_of_ids = validated_GET_rqst_params['id_list']
                else:
                    list_of_ids = None

                data_list = HealthcareServiceExpertise.get_serialized_rows_by_id(
                    rqst_id,
                    list_of_ids,
                    rqst_errors
                )
            elif 'name' in validated_GET_rqst_params:
                rqst_name = validated_GET_rqst_params['name']

                data_list = HealthcareServiceExpertise.get_serialized_rows_by_name(rqst_name, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response()

    parse_PUT_request_and_add_response = create_update_delete_method_logic

    accepted_GET_request_parameters = [
        "id",
        "name"
    ]
    parse_GET_request_and_add_response = read_method_logic
