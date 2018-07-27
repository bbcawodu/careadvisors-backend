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

    if 'tracking_no' in rqst_body:
        validated_params['tracking_no'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "tracking_no",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

    if 'user_name' in rqst_body:
        validated_params['user_name'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "user_name",
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

    if 'primary_care_physician' in rqst_body:
        validated_params['primary_care_physician'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "primary_care_physician",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

    if "appointment_datetime" in rqst_body:
        appointment_datetime = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "appointment_datetime",
            rqst_errors,
            none_allowed=True
        )
        validated_appointment_datetime = None
        if appointment_datetime:
            try:
                validated_appointment_datetime = datetime.datetime.strptime(appointment_datetime, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'appointment_datetime must be a properly formatted datetime string in UTC, eg. YYYY-MM-DDTHH:MM:SS. Value is : {}'.format(
                        appointment_datetime
                    )
                )
        validated_params['appointment_datetime'] = validated_appointment_datetime

    if 'policy_number' in rqst_body:
        validated_params['policy_number'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "policy_number",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

    if 'resource_case_number' in rqst_body:
        validated_params['resource_case_number'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "resource_case_number",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

    if 'expedite_benefits_organization_contact_name' in rqst_body:
        validated_params['expedite_benefits_organization_contact_name'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "expedite_benefits_organization_contact_name",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

    if 'expedite_benefits_organization_contact_phone' in rqst_body:
        validated_params['expedite_benefits_organization_contact_phone'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "expedite_benefits_organization_contact_phone",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

    if 'customer_service_success' in rqst_body:
        validated_params['customer_service_success'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "customer_service_success",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

    if 'case_status' in rqst_body:
        validated_params['case_status'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "case_status",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )
        if not rqst_errors and not validated_params['case_status']:
            validated_params['case_status'] = 'Not Available'


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

    if 'tracking_no' in rqst_body:
        validated_params['tracking_no'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "tracking_no",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

    if 'user_name' in rqst_body:
        validated_params['user_name'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "user_name",
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

    if 'primary_care_physician' in rqst_body:
        validated_params['primary_care_physician'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "primary_care_physician",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

    if "appointment_datetime" in rqst_body:
        appointment_datetime = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "appointment_datetime",
            rqst_errors,
            none_allowed=True
        )
        validated_appointment_datetime = None
        if appointment_datetime:
            try:
                validated_appointment_datetime = datetime.datetime.strptime(appointment_datetime, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'appointment_datetime must be a properly formatted datetime string in UTC, eg. YYYY-MM-DDTHH:MM:SS. Value is : {}'.format(
                        appointment_datetime
                    )
                )
        validated_params['appointment_datetime'] = validated_appointment_datetime

    if 'policy_number' in rqst_body:
        validated_params['policy_number'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "policy_number",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

    if 'resource_case_number' in rqst_body:
        validated_params['resource_case_number'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "resource_case_number",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

    if 'expedite_benefits_organization_contact_name' in rqst_body:
        validated_params['expedite_benefits_organization_contact_name'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "expedite_benefits_organization_contact_name",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

    if 'expedite_benefits_organization_contact_phone' in rqst_body:
        validated_params['expedite_benefits_organization_contact_phone'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "expedite_benefits_organization_contact_phone",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

    if 'customer_service_success' in rqst_body:
        validated_params['customer_service_success'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "customer_service_success",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

    if 'case_status' in rqst_body:
        validated_params['case_status'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "case_status",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )
        if not rqst_errors and not validated_params['case_status']:
            validated_params['case_status'] = 'Not Available'
