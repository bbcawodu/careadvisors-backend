from ...utils import clean_string_value_from_dict_object
from ...utils import clean_int_value_from_dict_object
from picmodels.services import add_web_traffic_calculator_data_instance_using_validated_params
from picmodels.services import modify_web_traffic_calculator_data_instance_using_validated_params
from picmodels.services import delete_web_traffic_calculator_data_instance_using_validated_params


def validate_rqst_params_and_add_instance(rqst_hospital_web_traffic_calculator_data_info, post_errors):
    add_hospital_web_traffic_calculator_data_params = validate_rqst_params(rqst_hospital_web_traffic_calculator_data_info, post_errors)

    web_traffic_data_obj = None
    if not post_errors:
        web_traffic_data_obj = add_web_traffic_calculator_data_instance_using_validated_params(
            add_hospital_web_traffic_calculator_data_params, post_errors)

    return web_traffic_data_obj


def validate_rqst_params(rqst_hospital_web_traffic_calculator_data_info, post_errors):

    return {
        "hospital_name": clean_string_value_from_dict_object(rqst_hospital_web_traffic_calculator_data_info, "root", "hospital_name", post_errors),
        "monthly_visits": clean_int_value_from_dict_object(rqst_hospital_web_traffic_calculator_data_info, "root", "monthly_visits", post_errors)
            }


def validate_rqst_params_and_modify_instance(rqst_hospital_web_traffic_calculator_data_info, post_errors):
    modify_hospital_web_traffic_calculator_data_params = validate_rqst_params(rqst_hospital_web_traffic_calculator_data_info, post_errors)
    rqst_hospital_web_traffic_calculator_data_id = clean_int_value_from_dict_object(rqst_hospital_web_traffic_calculator_data_info, "root", "Database ID", post_errors)

    web_traffic_data_obj = None
    if not post_errors:
        web_traffic_data_obj = modify_web_traffic_calculator_data_instance_using_validated_params(
            modify_hospital_web_traffic_calculator_data_params, rqst_hospital_web_traffic_calculator_data_id, post_errors)

    return web_traffic_data_obj


def validate_rqst_params_and_delete_instance(rqst_hospital_web_traffic_calculator_data_info, post_errors):
    rqst_hospital_web_traffic_calculator_data_id = clean_int_value_from_dict_object(rqst_hospital_web_traffic_calculator_data_info, "root", "Database ID", post_errors)

    if not post_errors:
        delete_web_traffic_calculator_data_instance_using_validated_params(rqst_hospital_web_traffic_calculator_data_id,
                                                                           post_errors)
