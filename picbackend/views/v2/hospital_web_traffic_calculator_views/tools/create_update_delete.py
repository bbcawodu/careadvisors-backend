from ...utils import clean_string_value_from_dict_object
from ...utils import clean_int_value_from_dict_object
from picmodels.services import add_web_traffic_calculator_data_instance_using_validated_params
from picmodels.services import modify_web_traffic_calculator_data_instance_using_validated_params
from picmodels.services import delete_web_traffic_calculator_data_instance_using_validated_params


def add_hospital_web_traffic_calculator_data_instance_using_api_rqst_params(response_raw_data, rqst_hospital_web_traffic_calculator_data_info, post_errors):
    add_hospital_web_traffic_calculator_data_params = get_hospital_web_traffic_calculator_data_mgmt_put_params(rqst_hospital_web_traffic_calculator_data_info, post_errors)

    if not post_errors:
        web_traffic_data_obj = add_web_traffic_calculator_data_instance_using_validated_params(
            add_hospital_web_traffic_calculator_data_params, post_errors)

        if not post_errors:
            response_raw_data['Data']["Database ID"] = web_traffic_data_obj.id

    return response_raw_data


def get_hospital_web_traffic_calculator_data_mgmt_put_params(rqst_hospital_web_traffic_calculator_data_info, post_errors):

    return {
        "hospital_name": clean_string_value_from_dict_object(rqst_hospital_web_traffic_calculator_data_info, "root", "hospital_name", post_errors),
        "monthly_visits": clean_int_value_from_dict_object(rqst_hospital_web_traffic_calculator_data_info, "root", "monthly_visits", post_errors)
            }


def modify_hospital_web_traffic_calculator_data_instance_using_api_rqst_params(response_raw_data, rqst_hospital_web_traffic_calculator_data_info, post_errors):
    modify_hospital_web_traffic_calculator_data_params = get_hospital_web_traffic_calculator_data_mgmt_put_params(rqst_hospital_web_traffic_calculator_data_info, post_errors)
    rqst_hospital_web_traffic_calculator_data_id = clean_int_value_from_dict_object(rqst_hospital_web_traffic_calculator_data_info, "root", "Database ID", post_errors)

    if len(post_errors) == 0:
        web_traffic_data_obj = modify_web_traffic_calculator_data_instance_using_validated_params(
            modify_hospital_web_traffic_calculator_data_params, rqst_hospital_web_traffic_calculator_data_id, post_errors)

        if not post_errors:
            response_raw_data['Data']["Database ID"] = web_traffic_data_obj.id

    return response_raw_data


def delete_hospital_web_traffic_calculator_data_instance_using_api_rqst_params(response_raw_data, rqst_hospital_web_traffic_calculator_data_info, post_errors):
    rqst_hospital_web_traffic_calculator_data_id = clean_int_value_from_dict_object(rqst_hospital_web_traffic_calculator_data_info, "root", "Database ID", post_errors)

    if not post_errors:
        delete_web_traffic_calculator_data_instance_using_validated_params(rqst_hospital_web_traffic_calculator_data_id,
                                                                           post_errors)
        if not post_errors:
            response_raw_data['Data']["Database ID"] = "Deleted"

    return response_raw_data
