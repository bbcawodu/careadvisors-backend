from picbackend.views.utils import clean_int_value_from_dict_object
from picbackend.views.utils import clean_string_value_from_dict_object
from picbackend.views.utils import clean_list_value_from_dict_object


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
    rqst_name = clean_string_value_from_dict_object(rqst_body, "root", "name", rqst_errors)
    validated_params["name"] = rqst_name

    if 'add_steps' in rqst_body:
        add_cm_steps = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "add_steps",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_cm_steps = []
        for step_id in add_cm_steps:
            if not isinstance(step_id, int):
                rqst_errors.append('Error: An step_id in \'add_steps\' is not an integer.')
                continue

            validated_cm_steps.append(step_id)

        validated_params['add_steps'] = validated_cm_steps


def validate_update_row_params(rqst_body, validated_params, rqst_errors):
    if "name" in rqst_body:
        rqst_name = clean_string_value_from_dict_object(rqst_body, "root", "name", rqst_errors, empty_string_allowed=True)
        validated_params["name"] = rqst_name

    if 'add_steps' in rqst_body:
        add_cm_steps = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "add_steps",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_cm_steps = []
        for step_id in add_cm_steps:
            if not isinstance(step_id, int):
                rqst_errors.append('Error: An step_id in \'add_steps\' is not an integer.')
                continue

            validated_cm_steps.append(step_id)

        validated_params['add_steps'] = validated_cm_steps
    elif 'remove_steps' in rqst_body:
        remove_cm_steps = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "remove_steps",
            rqst_errors
        )

        validated_cm_steps = []
        for step_id in remove_cm_steps:
            if not isinstance(step_id, int):
                rqst_errors.append('Error: An step_id in \'remove_steps\' is not an integer.')
                continue

            validated_cm_steps.append(step_id)

        validated_params['remove_steps'] = validated_cm_steps
