import datetime
import pytz
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

    if 'cm_client_id' in rqst_body:
        validated_params['cm_client_id'] = clean_int_value_from_dict_object(
            rqst_body,
            "root",
            "cm_client_id",
            rqst_errors,
            none_allowed=True
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

    if 'outcome' in rqst_body:
        validated_params['outcome'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "outcome",
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

    if "datetime_contacted" in rqst_body:
        datetime_contacted = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "datetime_contacted",
            rqst_errors,
            none_allowed=True
        )
        validated_datetime_contacted = None
        if datetime_contacted:
            try:
                validated_datetime_contacted = datetime.datetime.strptime(datetime_contacted, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'datetime_contacted must be a properly formatted datetime string in UTC, eg. YYYY-MM-DDTHH:MM:SS. Value is : {}'.format(
                        datetime_contacted)
                )
        validated_params['datetime_contacted'] = validated_datetime_contacted

    if 'contact_type' in rqst_body:
        validated_params['contact_type'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "contact_type",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )
    if "contact_type" not in validated_params or not validated_params['contact_type']:
        validated_params['contact_type'] = "not available"


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


    if 'cm_client_id' in rqst_body:
        validated_params['cm_client_id'] = clean_int_value_from_dict_object(
            rqst_body,
            "root",
            "cm_client_id",
            rqst_errors,
            none_allowed=True
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

    if 'outcome' in rqst_body:
        validated_params['outcome'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "outcome",
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

    if "datetime_contacted" in rqst_body:
        datetime_contacted = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "datetime_contacted",
            rqst_errors,
            none_allowed=True
        )
        validated_datetime_contacted = None
        if datetime_contacted:
            try:
                validated_datetime_contacted = datetime.datetime.strptime(datetime_contacted, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'datetime_contacted must be a properly formatted datetime string in UTC, eg. YYYY-MM-DDTHH:MM:SS. Value is : {}'.format(
                        datetime_contacted)
                )
        validated_params['datetime_contacted'] = validated_datetime_contacted

    if 'contact_type' in rqst_body:
        validated_params['contact_type'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "contact_type",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

        if not validated_params['contact_type']:
            validated_params['contact_type'] = "not available"
