from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..utils import JSONPUTRspMixin
from ..utils import JSONGETRspMixin
from picmodels.models import CareAdvisorCustomer
from .tools import validate_put_rqst_params
from .tools import retrieve_table_data_by_id
from .tools import retrieve_table_data_by_email
from .tools import retrieve_table_data_by_full_name
from .tools import retrieve_table_data_by_company_name
from .tools import retrieve_table_data_by_phone_number


# Need to abstract common variables in get and post class methods into class attributes
class CareAdvisorCustomerMgmtView(JSONPUTRspMixin, JSONGETRspMixin, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CareAdvisorCustomerMgmtView, self).dispatch(request, *args, **kwargs)

    def care_advisor_customer_mgmt_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        validated_params = validate_put_rqst_params(rqst_body, rqst_errors)

        if not rqst_errors:
            rqst_db_action = validated_params['db_action']
            care_advisor_customer_instance = None

            if rqst_db_action == "create_row":
                care_advisor_customer_instance = CareAdvisorCustomer.add_instance_using_validated_params(validated_params, rqst_errors)
            elif rqst_db_action == "update_row":
                care_advisor_customer_instance = CareAdvisorCustomer.modify_instance_using_validated_params(validated_params, rqst_errors)
            elif rqst_db_action == "delete_row":
                CareAdvisorCustomer.delete_instance_using_validated_params(validated_params, rqst_errors)
                if not rqst_errors:
                    response_raw_data['Data']["id"] = "deleted"

            if care_advisor_customer_instance:
                response_raw_data['Data']["id"] = care_advisor_customer_instance.id

    def care_advisor_customer_mgmt_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        def retrieve_data_by_primary_params_and_add_to_response():
            data_list = []

            if 'id' in validated_GET_rqst_params:
                rqst_staff_id = validated_GET_rqst_params['id']
                if rqst_staff_id != 'all':
                    list_of_ids = validated_GET_rqst_params['id_list']
                else:
                    list_of_ids = None

                data_list = retrieve_table_data_by_id(rqst_staff_id, list_of_ids, rqst_errors)
            elif 'full_name' in validated_GET_rqst_params:
                full_name = validated_GET_rqst_params['full_name']

                data_list = retrieve_table_data_by_full_name(full_name, rqst_errors)
            elif 'email' in validated_GET_rqst_params:
                list_of_emails = validated_GET_rqst_params['email_list']

                data_list = retrieve_table_data_by_email(list_of_emails, rqst_errors)
            elif 'company_name' in validated_GET_rqst_params:
                company_name = validated_GET_rqst_params['company_name']

                data_list = retrieve_table_data_by_company_name(company_name, rqst_errors)
            elif 'phone_number' in validated_GET_rqst_params:
                list_of_phone_numbers = validated_GET_rqst_params['phone_number_list']

                data_list = retrieve_table_data_by_phone_number(list_of_phone_numbers, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response()

    parse_PUT_request_and_add_response = care_advisor_customer_mgmt_put_logic

    accepted_GET_request_parameters = [
        "id",
        "full_name",
        "email",
        "company_name",
        "phone_number",
    ]
    parse_GET_request_and_add_response = care_advisor_customer_mgmt_get_logic
