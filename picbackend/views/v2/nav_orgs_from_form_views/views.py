from django.views.generic import View

from picbackend.views.utils import JSONGETRspMixin
from picbackend.views.utils import JSONPUTRspMixin
from picmodels.models import NavOrgsFromOnlineForm
from .tools import validate_put_rqst_params


# Need to abstract common variables in get and post class methods into class attributes
class NavOrgsFromOnlineFormMgmtView(JSONPUTRspMixin, JSONGETRspMixin, View):
    def nav_org_from_form_mgmt_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        validated_params = validate_put_rqst_params(rqst_body, rqst_errors)

        if not rqst_errors:
            db_action = validated_params['db_action']
            roq = None

            if db_action == "create":
                roq = NavOrgsFromOnlineForm.create_row_w_validated_params(
                    validated_params,
                    rqst_errors
                )
            elif db_action == "update":
                roq = NavOrgsFromOnlineForm.update_row_w_validated_params(
                    validated_params,
                    rqst_errors
                )
            elif db_action == "delete":
                NavOrgsFromOnlineForm.delete_row_w_validated_params(validated_params, rqst_errors)
                if not rqst_errors:
                    response_raw_data['Data']["row"] = "deleted"

            if roq:
                response_raw_data['Data']["row"] = roq.return_values_dict()

    def nav_org_from_form_mgmt_get_logic(self, request, validated_params, response_raw_data, rqst_errors):
        def retrieve_data_by_primary_params_and_add_to_response():
            data_list = []

            if 'id' in validated_params:
                data_list = NavOrgsFromOnlineForm.get_serialized_rows_by_id(validated_params, rqst_errors)
            elif 'email' in validated_params:
                data_list = NavOrgsFromOnlineForm.get_serialized_rows_by_email(validated_params, rqst_errors)
            elif 'company_name' in validated_params:
                data_list = NavOrgsFromOnlineForm.get_serialized_rows_by_company_name(validated_params, rqst_errors)
            elif 'phone_number' in validated_params:
                data_list = NavOrgsFromOnlineForm.get_serialized_rows_by_phone_number(validated_params, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response()

    parse_PUT_request_and_add_response = nav_org_from_form_mgmt_put_logic

    accepted_GET_request_parameters = [
        "id",
        "email",
        "company_name",
        "phone_number",
    ]
    parse_GET_request_and_add_response = nav_org_from_form_mgmt_get_logic
