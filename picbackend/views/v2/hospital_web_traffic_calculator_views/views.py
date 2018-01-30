from django.views.generic import View

from picbackend.views.utils import JSONGETRspMixin
from picbackend.views.utils import JSONPUTRspMixin
from picmodels.models import HospitalWebTrafficData
from .tools import validate_put_rqst_params


#Need to abstract common variables in get and post class methods into class attributes
class HospitalWebTrafficCalculatorDataMgrView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles healthcare carrier related requests
    """

    def hospital_web_traffic_calculator_data_mgr_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        validated_params = validate_put_rqst_params(rqst_body, rqst_errors)
        rqst_action = validated_params['rqst_action']

        # If there are no parsing errors, process PUT data based on database action
        if not rqst_errors:
            if rqst_action == "create":
                traffic_row = HospitalWebTrafficData.create_row_w_validated_params(validated_params, rqst_errors)

                if not rqst_errors:
                    response_raw_data['Data']["row"] = traffic_row.return_values_dict()
            elif rqst_action == "update":
                traffic_row = HospitalWebTrafficData.update_row_w_validated_params(validated_params, rqst_errors)

                if not rqst_errors:
                    response_raw_data['Data']["row"] = traffic_row.return_values_dict()
            elif rqst_action == "delete":
                HospitalWebTrafficData.delete_row_w_validated_params(validated_params, rqst_errors)

                if not rqst_errors:
                    response_raw_data['Data']["row"] = "Deleted"
            else:
                rqst_errors.append("No valid 'db_action' provided.")

    def hospital_web_traffic_calculator_data_mgr_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        def retrieve_data_by_primary_params_and_add_to_response():
            data_list = []

            if 'id' in validated_GET_rqst_params:
                rqst_hospital_web_traffic_calculator_data_id = validated_GET_rqst_params['id']
                if rqst_hospital_web_traffic_calculator_data_id != 'all':
                    list_of_ids = validated_GET_rqst_params['id_list']
                else:
                    list_of_ids = []

                data_list = HospitalWebTrafficData.retrieve_hospital_traffic_data_by_id(
                    rqst_hospital_web_traffic_calculator_data_id,
                    list_of_ids,
                    rqst_errors
                )
            elif 'hospital_name' in validated_GET_rqst_params:
                rqst_hospital_name = validated_GET_rqst_params['hospital_name']

                data_list = HospitalWebTrafficData.retrieve_hospital_traffic_data_by_name(rqst_hospital_name, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response()

    parse_PUT_request_and_add_response = hospital_web_traffic_calculator_data_mgr_put_logic

    accepted_GET_request_parameters = [
        "id",
        "hospital_name"
    ]
    parse_GET_request_and_add_response = hospital_web_traffic_calculator_data_mgr_get_logic
