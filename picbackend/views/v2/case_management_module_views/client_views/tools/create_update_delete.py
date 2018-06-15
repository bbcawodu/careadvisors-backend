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

    if "address_line_1" in rqst_body:
        address_line_1 = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "address_line_1",
            rqst_errors,
            empty_string_allowed=True
        )
        validated_params["address_line_1"] = address_line_1

    if "address_line_2" in rqst_body:
        address_line_2 = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "address_line_2",
            rqst_errors,
            empty_string_allowed=True
        )
        if address_line_2 is None:
            address_line_2 = ''
        validated_params["address_line_2"] = address_line_2

    if "city" in rqst_body:
        city = clean_string_value_from_dict_object(rqst_body, "root", "city", rqst_errors, empty_string_allowed=True)
        validated_params["city"] = city

    if "state_province" in rqst_body:
        state_province = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "state_province",
            rqst_errors,
            empty_string_allowed=True
        )
        validated_params["state_province"] = state_province

    if "zipcode" in rqst_body:
        zipcode = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "zipcode",
            rqst_errors,
            empty_string_allowed=True
        )
        validated_params["zipcode"] = zipcode

    if 'add_cm_sequences' in rqst_body:
        add_cm_sequences = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "add_cm_sequences",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_cm_sequence_ids = []
        for cm_sequence_id in add_cm_sequences:
            if not isinstance(cm_sequence_id, int):
                rqst_errors.append('Error: A cm_sequence_id in \'add_cm_sequences\' is not an integer.')
                continue

            validated_cm_sequence_ids.append(cm_sequence_id)

        validated_params['add_cm_sequences'] = validated_cm_sequence_ids


def validate_update_row_params(rqst_body, validated_params, rqst_errors):
    if "name" in rqst_body:
        rqst_name = clean_string_value_from_dict_object(rqst_body, "root", "name", rqst_errors, empty_string_allowed=True)
        validated_params["name"] = rqst_name

    if "address_line_1" in rqst_body:
        address_line_1 = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "address_line_1",
            rqst_errors,
            empty_string_allowed=True
        )
        validated_params["address_line_1"] = address_line_1

    if "address_line_2" in rqst_body:
        address_line_2 = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "address_line_2",
            rqst_errors,
            empty_string_allowed=True
        )
        if address_line_2 is None:
            address_line_2 = ''
        validated_params["address_line_2"] = address_line_2

    if "city" in rqst_body:
        city = clean_string_value_from_dict_object(rqst_body, "root", "city", rqst_errors, empty_string_allowed=True)
        validated_params["city"] = city

    if "state_province" in rqst_body:
        state_province = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "state_province",
            rqst_errors,
            empty_string_allowed=True
        )
        validated_params["state_province"] = state_province

    if "zipcode" in rqst_body:
        zipcode = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "zipcode",
            rqst_errors,
            empty_string_allowed=True
        )
        validated_params["zipcode"] = zipcode

    if 'add_cm_sequences' in rqst_body:
        add_cm_sequences = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "add_cm_sequences",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_cm_sequence_ids = []
        for cm_sequence_id in add_cm_sequences:
            if not isinstance(cm_sequence_id, int):
                rqst_errors.append('Error: A cm_sequence_id in \'add_cm_sequences\' is not an integer.')
                continue

            validated_cm_sequence_ids.append(cm_sequence_id)

        validated_params['add_cm_sequences'] = validated_cm_sequence_ids
    elif 'remove_base_locations' in rqst_body:
        remove_cm_sequences = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "remove_cm_sequences",
            rqst_errors
        )

        validated_cm_sequence_ids = []
        for cm_sequence_id in remove_cm_sequences:
            if not isinstance(cm_sequence_id, int):
                rqst_errors.append('Error: A cm_sequence_id in \'remove_cm_sequences\' is not an integer.')
                continue

            validated_cm_sequence_ids.append(cm_sequence_id)

        validated_params['remove_cm_sequences'] = validated_cm_sequence_ids
