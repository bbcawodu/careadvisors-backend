from picbackend.views.utils import clean_int_value_from_dict_object
from picbackend.views.utils import clean_string_value_from_dict_object


def validate_put_rqst_params(rqst_body, rqst_errors):
    validated_params = {
        'rqst_action': clean_string_value_from_dict_object(rqst_body, "root", "db_action", rqst_errors)
    }

    rqst_action = validated_params['rqst_action']

    if rqst_action == 'create':
        validate_create_row_params(rqst_body, validated_params, rqst_errors)
    elif rqst_action == 'update':
        validated_params['rqst_id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)
        validate_update_row_params(rqst_body, validated_params, rqst_errors)
    elif rqst_action == 'delete':
        validated_params['rqst_id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)

    return validated_params


def validate_create_row_params(rqst_body, validated_params, rqst_errors):
    validated_params["hospital_name"] = clean_string_value_from_dict_object(rqst_body, "root", "hospital_name", rqst_errors)
    validated_params["monthly_visits"] = clean_int_value_from_dict_object(rqst_body, "root", "monthly_visits", rqst_errors)


def validate_update_row_params(rqst_body, validated_params, rqst_errors):
    if "hospital_name" in rqst_body:
        validated_params["hospital_name"] = clean_string_value_from_dict_object(rqst_body, "root", "hospital_name", rqst_errors)

    if "monthly_visits" in rqst_body:
        validated_params["monthly_visits"] = clean_int_value_from_dict_object(rqst_body, "root", "monthly_visits", rqst_errors)
