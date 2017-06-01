from django.views.generic import View
from django.utils.decorators import method_decorator
from ..utils import clean_string_value_from_dict_object
from picmodels.models import HospitalWebTrafficData
from .tools import add_hospital_web_traffic_calculator_data_instance_using_api_rqst_params
from .tools import modify_hospital_web_traffic_calculator_data_instance_using_api_rqst_params
from .tools import delete_hospital_web_traffic_calculator_data_instance_using_api_rqst_params
from .tools import retrieve_hospital_web_traffic_calculator_data_by_id
from .tools import retrieve_web_traffic_calculator_data_by_hospital_name
from django.views.decorators.csrf import csrf_exempt
from ..base import JSONPUTRspMixin
from ..base import JSONGETRspMixin


#Need to abstract common variables in get and post class methods into class attributes
class HospitalWebTrafficCalculatorDataMgrView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles healthcare carrier related requests
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(HospitalWebTrafficCalculatorDataMgrView, self).dispatch(request, *args, **kwargs)

    def hospital_web_traffic_calculator_data_mgr_put_logic(self, post_data, response_raw_data, post_errors):
        # Retrieve database action from post data
        rqst_action = clean_string_value_from_dict_object(post_data, "root", "Database Action", post_errors)

        # If there are no parsing errors, process PUT data based on database action
        if not post_errors:
            if rqst_action == "Instance Addition":
                response_raw_data = add_hospital_web_traffic_calculator_data_instance_using_api_rqst_params(response_raw_data, post_data, post_errors)
            elif rqst_action == "Instance Modification":
                response_raw_data = modify_hospital_web_traffic_calculator_data_instance_using_api_rqst_params(response_raw_data, post_data, post_errors)
            elif rqst_action == "Instance Deletion":
                response_raw_data = delete_hospital_web_traffic_calculator_data_instance_using_api_rqst_params(response_raw_data, post_data, post_errors)
            else:
                post_errors.append("No valid 'Database Action' provided.")

        return response_raw_data, post_errors

    def hospital_web_traffic_calculator_data_mgr_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        web_traffic_calculator_data = HospitalWebTrafficData.objects.all()

        if 'id' in search_params:
            rqst_hospital_web_traffic_calculator_data_id = search_params['id']
            if rqst_hospital_web_traffic_calculator_data_id != 'all':
                list_of_ids = search_params['id list']
            else:
                list_of_ids = None
            response_raw_data, rqst_errors = retrieve_hospital_web_traffic_calculator_data_by_id(response_raw_data,
                                                                                                 rqst_errors,
                                                                                                 web_traffic_calculator_data,
                                                                                                 rqst_hospital_web_traffic_calculator_data_id,
                                                                                                 list_of_ids)
        elif 'hospital_name' in search_params:
            rqst_hospital_name = search_params['hospital_name']

            response_raw_data, rqst_errors = retrieve_web_traffic_calculator_data_by_hospital_name(response_raw_data,
                                                                                                   rqst_errors,
                                                                                                   web_traffic_calculator_data,
                                                                                                   rqst_hospital_name)

        return response_raw_data, rqst_errors

    put_logic_function = hospital_web_traffic_calculator_data_mgr_put_logic
    get_logic_function = hospital_web_traffic_calculator_data_mgr_get_logic
