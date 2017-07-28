"""
Defines views that handle Patient Innovation Center Staff based requests
API Version 2
"""


from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..utils import JSONPUTRspMixin
from ..utils import JSONGETRspMixin
from .tools import validate_put_rqst_params
from picmodels.services.care_advisor_customer_model_services import add_instance_using_validated_params
from picmodels.services.care_advisor_customer_model_services import modify_instance_using_validated_params
from picmodels.services.care_advisor_customer_model_services import delete_instance_using_validated_params
from .tools import retrieve_table_data_by_id
from .tools import retrieve_staff_data_by_f_and_l_name
from .tools import retrieve_staff_data_by_email
from .tools import retrieve_staff_data_by_first_name
from .tools import retrieve_staff_data_by_last_name


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
                care_advisor_customer_instance = add_instance_using_validated_params(validated_params, rqst_errors)
            elif rqst_db_action == "update_row":
                care_advisor_customer_instance = modify_instance_using_validated_params(validated_params, rqst_errors)
            elif rqst_db_action == "delete_row":
                delete_instance_using_validated_params(validated_params, rqst_errors)
                if not rqst_errors:
                    response_raw_data['Data']["id"] = "deleted"

            if care_advisor_customer_instance:
                response_raw_data['Data']["id"] = care_advisor_customer_instance.id

    def care_advisor_customer_mgmt_get_logic(self, request, validated_params, response_raw_data, rqst_errors):
        def retrieve_data_by_primary_params_and_add_to_response():
            data_list = []

            if 'first_name' in validated_params and 'last_name' in validated_params:
                rqst_first_name = validated_params['first_name']
                rqst_last_name = validated_params['last_name']

                data_list = retrieve_staff_data_by_f_and_l_name(rqst_first_name, rqst_last_name, rqst_errors)
            elif 'email' in validated_params:
                list_of_emails = validated_params['email_list']

                data_list = retrieve_staff_data_by_email(list_of_emails, rqst_errors)
            elif 'first_name' in validated_params:
                list_of_first_names = validated_params['first_name_list']

                data_list = retrieve_staff_data_by_first_name(list_of_first_names, rqst_errors)
            elif 'last_name' in validated_params:
                list_of_last_names = validated_params['last_name_list']

                data_list = retrieve_staff_data_by_last_name(list_of_last_names, rqst_errors)
            elif 'id' in validated_params:
                rqst_staff_id = validated_params['id']
                if rqst_staff_id != 'all':
                    list_of_ids = validated_params['id_list']
                else:
                    list_of_ids = None

                data_list = retrieve_table_data_by_id(rqst_staff_id, list_of_ids, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response()

    put_logic_function = care_advisor_customer_mgmt_put_logic

    accepted_get_parameters = [
        "id",
        "first_name",
        "last_name",
        "email",
        "company_name",
        "phone_number",
    ]
    get_logic_function = care_advisor_customer_mgmt_get_logic
