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
        validated_params['id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)
        validate_update_row_params(rqst_body, validated_params, rqst_errors)
    elif rqst_action == 'delete':
        validated_params['id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)

    return validated_params


def validate_create_row_params(rqst_body, validated_params, rqst_errors):
    validated_params['consumer_id'] = clean_int_value_from_dict_object(
        rqst_body,
        "root",
        "consumer_id",
        rqst_errors
    )

    validated_params['navigator_id'] = clean_int_value_from_dict_object(
        rqst_body,
        "root",
        "navigator_id",
        rqst_errors
    )

    if 'notes' in rqst_body:
        validated_params['notes'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "notes",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

    if 'status' in rqst_body:
        validated_params['status'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "status",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )
    if 'status' not in validated_params or not validated_params['status']:
        validated_params['status'] = "not available"

    if 'severity' in rqst_body:
        validated_params['severity'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "severity",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )
    if "severity" not in validated_params or not validated_params['severity']:
        validated_params['severity'] = "not available"


def validate_update_row_params(rqst_body, validated_params, rqst_errors):
    if 'consumer_id' in rqst_body:
        validated_params['consumer_id'] = clean_int_value_from_dict_object(
            rqst_body,
            "root",
            "consumer_id",
            rqst_errors
        )

    if 'navigator_id' in rqst_body:
        validated_params['navigator_id'] = clean_int_value_from_dict_object(
            rqst_body,
            "root",
            "navigator_id",
            rqst_errors
        )

    if 'notes' in rqst_body:
        validated_params['notes'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "notes",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

    if 'status' in rqst_body:
        validated_params['status'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "status",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

        if not validated_params['status']:
            validated_params['status'] = "not available"

    if 'severity' in rqst_body:
        validated_params['severity'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "severity",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

        if not validated_params['severity']:
            validated_params['severity'] = "not available"
