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
    validated_params['step_name'] = clean_string_value_from_dict_object(
        rqst_body,
        "root",
        "step_name",
        rqst_errors
    )

    validated_params['step_class_name'] = clean_string_value_from_dict_object(
        rqst_body,
        "root",
        "step_class_name",
        rqst_errors
    )

    if 'step_table_name' in rqst_body:
        validated_params['step_table_name'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "step_tables_name",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

    validated_params['step_number'] = clean_int_value_from_dict_object(
        rqst_body,
        "root",
        "step_number",
        rqst_errors
    )
    if validated_params['step_number'] and validated_params['step_number'] < 0:
        rqst_errors.append(
            "Value for 'step_number' must be greater than 0. Given value is: {}".format(
                validated_params['step_number']
            )
        )


def validate_update_row_params(rqst_body, validated_params, rqst_errors):
    if 'step_name' in rqst_body:
        validated_params['step_name'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "step_name",
            rqst_errors
        )

    if 'step_class_name' in rqst_body:
        validated_params['step_class_name'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "step_class_name",
            rqst_errors
        )

    if 'step_table_name' in rqst_body:
        validated_params['step_table_name'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "step_tables_name",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

    if 'step_number' in rqst_body:
        validated_params['step_number'] = clean_int_value_from_dict_object(
            rqst_body,
            "root",
            "step_number",
            rqst_errors
        )
        if validated_params['step_number'] and validated_params['step_number'] < 0:
            rqst_errors.append(
                "Value for 'step_number' must be greater than 0. Given value is: {}".format(
                    validated_params['step_number']
                )
            )
