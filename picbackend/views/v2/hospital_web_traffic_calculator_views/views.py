from django.views.generic import View
from ..utils import clean_string_value_from_dict_object
from picmodels.models import HospitalWebTrafficData
from .tools import validate_rqst_params_and_add_instance
from .tools import validate_rqst_params_and_modify_instance
from .tools import validate_rqst_params_and_delete_instance
from .tools import retrieve_hospital_web_traffic_calculator_data_by_id
from .tools import retrieve_web_traffic_calculator_data_by_hospital_name
from ..utils import JSONPUTRspMixin
from ..utils import JSONGETRspMixin


#Need to abstract common variables in get and post class methods into class attributes
class HospitalWebTrafficCalculatorDataMgrView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles healthcare carrier related requests
    """

    def hospital_web_traffic_calculator_data_mgr_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        # Retrieve database action from post data
        rqst_action = clean_string_value_from_dict_object(rqst_body, "root", "Database Action", rqst_errors)

        # If there are no parsing errors, process PUT data based on database action
        if not rqst_errors:
            if rqst_action == "Instance Addition":
                web_traffic_data_obj = validate_rqst_params_and_add_instance(rqst_body, rqst_errors)

                if not rqst_errors:
                    response_raw_data['Data']["Database ID"] = web_traffic_data_obj.id
            elif rqst_action == "Instance Modification":
                web_traffic_data_obj = validate_rqst_params_and_modify_instance(rqst_body, rqst_errors)

                if not rqst_errors:
                    response_raw_data['Data']["Database ID"] = web_traffic_data_obj.id
            elif rqst_action == "Instance Deletion":
                validate_rqst_params_and_delete_instance(rqst_body, rqst_errors)

                if not rqst_errors:
                    response_raw_data['Data']["Database ID"] = "Deleted"
            else:
                rqst_errors.append("No valid 'Database Action' provided.")

    def hospital_web_traffic_calculator_data_mgr_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        web_traffic_calculator_data = HospitalWebTrafficData.objects.all()

        def retrieve_data_by_primary_params_and_add_to_response(db_objects):
            data_list = []

            if 'id' in validated_GET_rqst_params:
                rqst_hospital_web_traffic_calculator_data_id = validated_GET_rqst_params['id']
                if rqst_hospital_web_traffic_calculator_data_id != 'all':
                    list_of_ids = validated_GET_rqst_params['id_list']
                else:
                    list_of_ids = []
                data_list = retrieve_hospital_web_traffic_calculator_data_by_id(db_objects,
                                                                                rqst_hospital_web_traffic_calculator_data_id,
                                                                                list_of_ids, rqst_errors)
            elif 'hospital_name' in validated_GET_rqst_params:
                rqst_hospital_name = validated_GET_rqst_params['hospital_name']

                data_list = retrieve_web_traffic_calculator_data_by_hospital_name(db_objects,
                                                                                  rqst_hospital_name, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response(web_traffic_calculator_data)

    parse_PUT_request_and_add_response = hospital_web_traffic_calculator_data_mgr_put_logic

    accepted_GET_request_parameters = [
        "id",
        "hospital_name"
    ]
    parse_GET_request_and_add_response = hospital_web_traffic_calculator_data_mgr_get_logic
