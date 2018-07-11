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

    validated_params['cm_client_id'] = clean_int_value_from_dict_object(
        rqst_body,
        "root",
        "cm_client_id",
        rqst_errors,
        none_allowed=True
    )

    validated_params['cm_sequence_id'] = clean_int_value_from_dict_object(
        rqst_body,
        "root",
        "cm_sequence_id",
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

    if "datetime_completed" in rqst_body:
        datetime_completed = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "datetime_completed",
            rqst_errors,
            none_allowed=True
        )
        validated_datetime_completed = None
        if datetime_completed:
            try:
                validated_datetime_completed = datetime.datetime.strptime(datetime_completed, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'datetime_completed must be a properly formatted datetime string in UTC, eg. YYYY-MM-DDTHH:MM:SS. Value is : {}'.format(
                        datetime_completed)
                )
        validated_params['datetime_completed'] = validated_datetime_completed

    if "client_appointment_datetime" in rqst_body:
        client_appointment_datetime = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "client_appointment_datetime",
            rqst_errors,
            none_allowed=True
        )
        validated_client_appointment_datetime = None
        if client_appointment_datetime:
            try:
                validated_client_appointment_datetime = datetime.datetime.strptime(client_appointment_datetime, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'client_appointment_datetime must be a properly formatted datetime string in UTC, eg. YYYY-MM-DDTHH:MM:SS. Value is : {}'.format(
                        client_appointment_datetime
                    )
                )
        validated_params['client_appointment_datetime'] = validated_client_appointment_datetime


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

    if "cm_sequence_id" in rqst_body:
        validated_params['cm_sequence_id'] = clean_int_value_from_dict_object(
            rqst_body,
            "root",
            "cm_sequence_id",
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

    if "datetime_completed" in rqst_body:
        datetime_completed = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "datetime_completed",
            rqst_errors,
            none_allowed=True
        )
        validated_datetime_completed = None
        if datetime_completed:
            try:
                validated_datetime_completed = datetime.datetime.strptime(datetime_completed, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'datetime_completed must be a properly formatted datetime string in UTC, eg. YYYY-MM-DDTHH:MM:SS. Value is : {}'.format(
                        datetime_completed)
                )
        validated_params['datetime_completed'] = validated_datetime_completed

    if "client_appointment_datetime" in rqst_body:
        client_appointment_datetime = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "client_appointment_datetime",
            rqst_errors,
            none_allowed=True
        )
        validated_client_appointment_datetime = None
        if client_appointment_datetime:
            try:
                validated_client_appointment_datetime = datetime.datetime.strptime(client_appointment_datetime, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'client_appointment_datetime must be a properly formatted datetime string in UTC, eg. YYYY-MM-DDTHH:MM:SS. Value is : {}'.format(
                        client_appointment_datetime
                    )
                )
        validated_params['client_appointment_datetime'] = validated_client_appointment_datetime
