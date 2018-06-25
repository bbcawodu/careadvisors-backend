import datetime
import re
import urllib
import json
from picmodels.models import HealthcarePlan


def validate_get_rqst_parameter_id(get_rqst_params, validated_params, rqst_errors):
    param_name = 'id'

    if param_name in get_rqst_params:
        if get_rqst_params[param_name] != "all":
            validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)
        else:
            validated_params[param_name] = get_rqst_params[param_name]


def validate_get_rqst_parameter_first_name(get_rqst_params, validated_params, rqst_errors):
    param_name = 'first_name'

    if param_name in get_rqst_params:
        validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_last_name(get_rqst_params, validated_params, rqst_errors):
    param_name = 'last_name'

    if param_name in get_rqst_params:
        validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_email(get_rqst_params, validated_params, rqst_errors):
    param_name = 'email'

    if param_name in get_rqst_params:
        validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_mpn(get_rqst_params, validated_params, rqst_errors):
    param_name = 'mpn'

    if param_name in get_rqst_params:
        validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_region(get_rqst_params, validated_params, rqst_errors):
    param_name = 'region'

    if param_name in get_rqst_params:
        validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_location(get_rqst_params, validated_params, rqst_errors):
    param_name = 'location'

    if param_name in get_rqst_params:
        validate_url_encoded_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_locationid(get_rqst_params, validated_params, rqst_errors):
    param_name = 'location_id'

    if param_name in get_rqst_params:
        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)
        if not rqst_errors:
            validated_params[param_name] = get_rqst_params[param_name]


def validate_get_rqst_parameter_nav_id(get_rqst_params, validated_params, rqst_errors):
    param_name = 'nav_id'

    if param_name in get_rqst_params:
        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)
        if not rqst_errors:
            validated_params[param_name] = get_rqst_params[param_name]


def validate_get_rqst_parameter_consumer_id(get_rqst_params, validated_params, rqst_errors):
    param_name = 'consumer_id'

    if param_name in get_rqst_params:
        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)
        if not rqst_errors:
            validated_params[param_name] = get_rqst_params[param_name]


def validate_get_rqst_parameter_cm_client_id(get_rqst_params, validated_params, rqst_errors):
    param_name = 'cm_client_id'

    if param_name in get_rqst_params:
        if get_rqst_params[param_name] != "all":
            validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)
        else:
            validated_params[param_name] = get_rqst_params[param_name]


def validate_get_rqst_parameter_cm_sequence_id(get_rqst_params, validated_params, rqst_errors):
    param_name = 'cm_sequence_id'

    if param_name in get_rqst_params:
        if get_rqst_params[param_name] != "all":
            validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)
        else:
            validated_params[param_name] = get_rqst_params[param_name]


def validate_get_rqst_parameter_referring_cm_client_id(get_rqst_params, validated_params, rqst_errors):
    param_name = 'referring_cm_client_id'

    if param_name in get_rqst_params:
        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)
        if not rqst_errors:
            validated_params[param_name] = get_rqst_params[param_name]


def validate_get_rqst_parameter_approved_cm_client_id(get_rqst_params, validated_params, rqst_errors):
    param_name = 'approved_cm_client_id'

    if param_name in get_rqst_params:
        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)
        if not rqst_errors:
            validated_params[param_name] = get_rqst_params[param_name]


def validate_get_rqst_parameter_staff_id(get_rqst_params, validated_params, rqst_errors):
    param_name = 'staff_id'

    if param_name in get_rqst_params and get_rqst_params[param_name] != "all":
        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)
        if not rqst_errors:
            validated_params[param_name] = get_rqst_params[param_name]


def validate_get_rqst_parameter_county(get_rqst_params, validated_params, rqst_errors):
    param_name = 'county'

    if param_name in get_rqst_params:
        validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_zipcode(get_rqst_params, validated_params, rqst_errors):
    param_name = "zipcode"

    if param_name in get_rqst_params:
        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)
        if not rqst_errors:
            validated_params[param_name] = get_rqst_params[param_name]


def validate_get_rqst_parameter_time_delta_in_days(get_rqst_params, validated_params, rqst_errors):
    param_name = 'time_delta_in_days'

    if param_name in get_rqst_params:
        validate_time_delta_in_days_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_start_date(get_rqst_params, validated_params, rqst_errors):
    param_name = 'start_date'

    if param_name in get_rqst_params:
        validate_yyyy_mm_dd_timestamp_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_end_date(get_rqst_params, validated_params, rqst_errors):
    param_name = 'end_date'

    if param_name in get_rqst_params:
        validate_yyyy_mm_dd_timestamp_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        if validated_params[param_name]:
            validated_params[param_name] = validated_params[param_name].replace(hour=23, minute=59, second=59, microsecond=0)


def validate_get_rqst_parameter_date_created_start(get_rqst_params, validated_params, rqst_errors):
    param_name = 'date_created_start'

    if param_name in get_rqst_params:
        validate_yyyy_mm_dd_timestamp_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_date_created_end(get_rqst_params, validated_params, rqst_errors):
    param_name = 'date_created_end'

    if param_name in get_rqst_params:
        validate_yyyy_mm_dd_timestamp_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        if validated_params[param_name]:
            validated_params[param_name] = validated_params[param_name].replace(hour=23, minute=59, second=59, microsecond=0)


def validate_get_rqst_parameter_date_modified_start(get_rqst_params, validated_params, rqst_errors):
    param_name = 'date_modified_start'

    if param_name in get_rqst_params:
        validate_yyyy_mm_dd_timestamp_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_date_modified_end(get_rqst_params, validated_params, rqst_errors):
    param_name = 'date_modified_end'

    if param_name in get_rqst_params:
        validate_yyyy_mm_dd_timestamp_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        if validated_params[param_name]:
            validated_params[param_name] = validated_params[param_name].replace(hour=23, minute=59, second=59, microsecond=0)


def validate_get_rqst_parameter_datetime_contacted_start_date(get_rqst_params, validated_params, rqst_errors):
    param_name = 'datetime_contacted_start_date'

    if param_name in get_rqst_params:
        validate_yyyy_mm_dd_timestamp_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_datetime_contacted_end_date(get_rqst_params, validated_params, rqst_errors):
    param_name = 'datetime_contacted_end_date'

    if param_name in get_rqst_params:
        validate_yyyy_mm_dd_timestamp_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        if validated_params[param_name]:
            validated_params[param_name] = validated_params[param_name].replace(hour=23, minute=59, second=59, microsecond=0)


def validate_get_rqst_parameter_datetime_completed_start_date(get_rqst_params, validated_params, rqst_errors):
    param_name = 'datetime_completed_start_date'

    if param_name in get_rqst_params:
        validate_yyyy_mm_dd_timestamp_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_datetime_completed_end_date(get_rqst_params, validated_params, rqst_errors):
    param_name = 'datetime_completed_end_date'

    if param_name in get_rqst_params:
        validate_yyyy_mm_dd_timestamp_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        if validated_params[param_name]:
            validated_params[param_name] = validated_params[param_name].replace(hour=23, minute=59, second=59, microsecond=0)


def validate_get_rqst_parameter_is_cps_consumer(get_rqst_params, validated_params, rqst_errors):
    param_name = 'is_cps_consumer'

    if param_name in get_rqst_params:
        validate_bool_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_has_hospital_info(get_rqst_params, validated_params, rqst_errors):
    param_name = 'has_hospital_info'

    if param_name in get_rqst_params:
        validate_bool_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_partner_id(get_rqst_params, validated_params, rqst_errors):
    param_name = 'partner_id'

    if param_name in get_rqst_params:
        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)
        if not rqst_errors:
            validated_params[param_name] = get_rqst_params[param_name]


def validate_get_rqst_parameter_fields(get_rqst_params, validated_params, rqst_errors):
    param_name = 'fields'

    if param_name in get_rqst_params:
        validate_url_encoded_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validated_params['fields list'] = re.findall(r"[@\w. '-]+", validated_params['fields'])
        if not validated_params['fields list']:
            rqst_errors.append('Invalid fields parameter, field parameters must be a url encoded ascii strings.')


def validate_get_rqst_parameter_page(get_rqst_params, validated_params, rqst_errors):
    param_name = 'page'

    if param_name in get_rqst_params:
        validate_int_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_group_by(get_rqst_params, validated_params, rqst_errors):
    param_name = 'group_by'

    if param_name in get_rqst_params:
        validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_nav_location_tags(get_rqst_params, validated_params, rqst_errors):
    param_name = 'nav_location_tags'

    if param_name in get_rqst_params:
        validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_is_cps_location(get_rqst_params, validated_params, rqst_errors):
    param_name = 'is_cps_location'

    if param_name in get_rqst_params:
        validate_bool_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_name(get_rqst_params, validated_params, rqst_errors):
    param_name = 'name'

    if param_name in get_rqst_params:
        validate_url_encoded_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_user_name(get_rqst_params, validated_params, rqst_errors):
    param_name = 'user_name'

    if param_name in get_rqst_params:
        validate_url_encoded_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_tracking_no(get_rqst_params, validated_params, rqst_errors):
    param_name = 'tracking_no'

    if param_name in get_rqst_params:
        validate_url_encoded_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_intent(get_rqst_params, validated_params, rqst_errors):
    param_name = 'intent'

    if param_name in get_rqst_params:
        validate_url_encoded_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_status(get_rqst_params, validated_params, rqst_errors):
    param_name = 'status'

    if param_name in get_rqst_params:
        validate_url_encoded_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_contact_type(get_rqst_params, validated_params, rqst_errors):
    param_name = 'contact_type'

    if param_name in get_rqst_params:
        validate_url_encoded_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_severity(get_rqst_params, validated_params, rqst_errors):
    param_name = 'severity'

    if param_name in get_rqst_params:
        validate_url_encoded_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_state(get_rqst_params, validated_params, rqst_errors):
    param_name = "state"

    if param_name in get_rqst_params:
        validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_has_sample_id_card(get_rqst_params, validated_params, rqst_errors):
    param_name = 'has_sample_id_card'

    if param_name in get_rqst_params:
        validate_bool_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_carrier_id(get_rqst_params, validated_params, rqst_errors):
    param_name = 'carrier_id'

    if param_name in get_rqst_params:
        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)
        if not rqst_errors:
            validated_params[param_name] = get_rqst_params[param_name]


def validate_get_rqst_parameter_carrier_state(get_rqst_params, validated_params, rqst_errors):
    param_name = "carrier_state"

    if param_name in get_rqst_params:
        validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_carrier_name(get_rqst_params, validated_params, rqst_errors):
    param_name = 'carrier_name'

    if param_name in get_rqst_params:
        validate_url_encoded_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_accepted_location_id(get_rqst_params, validated_params, rqst_errors):
    param_name = 'accepted_location_id'

    if param_name in get_rqst_params:
        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)
        if not rqst_errors:
            validated_params[param_name] = get_rqst_params[param_name]


def validate_get_rqst_parameter_network_name(get_rqst_params, validated_params, rqst_errors):
    param_name = 'network_name'

    if param_name in get_rqst_params:
        validate_url_encoded_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_network_id(get_rqst_params, validated_params, rqst_errors):
    param_name = 'network_id'

    if param_name in get_rqst_params:
        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)
        if not rqst_errors:
            validated_params[param_name] = get_rqst_params[param_name]


def validate_get_rqst_parameter_premium_type(get_rqst_params, validated_params, rqst_errors):
    param_name = 'premium_type'

    if param_name in get_rqst_params:
        validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        # for premium_type in validated_params['premium_type_list']:
        #     dummy_plan_object = HealthcarePlan(premium_type=premium_type)
        #     if not dummy_plan_object.check_premium_choices():
        #         rqst_errors.append('The following is an invalid premium_type : {}'.format(premium_type))


def validate_get_rqst_parameter_include_summary_report(get_rqst_params, validated_params, rqst_errors):
    param_name = 'include_summary_report'

    if param_name in get_rqst_params:
        validate_bool_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_include_detailed_report(get_rqst_params, validated_params, rqst_errors):
    param_name = 'include_detailed_report'

    if param_name in get_rqst_params:
        validate_bool_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_question(get_rqst_params, validated_params, rqst_errors):
    param_name = 'question'

    if param_name in get_rqst_params:
        validate_url_encoded_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_gen_concern_name(get_rqst_params, validated_params, rqst_errors):
    param_name = 'gen_concern_name'

    if param_name in get_rqst_params:
        validate_url_encoded_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_gen_concern_id(get_rqst_params, validated_params, rqst_errors):
    param_name = 'gen_concern_id'

    if param_name in get_rqst_params:
        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)
        if not rqst_errors:
            validated_params[param_name] = get_rqst_params[param_name]


def validate_get_rqst_parameter_gen_concern_id_subset(get_rqst_params, validated_params, rqst_errors):
    param_name = 'gen_concern_id_subset'

    if param_name in get_rqst_params:
        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)
        if not rqst_errors:
            validated_params[param_name] = get_rqst_params[param_name]


def validate_get_rqst_parameter_hospital_name(get_rqst_params, validated_params, rqst_errors):
    param_name = 'hospital_name'

    if param_name in get_rqst_params:
        validate_url_encoded_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_family_size(get_rqst_params, validated_params, rqst_errors):
    param_name = 'family_size'

    if param_name in get_rqst_params:
        validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)
        if not rqst_errors:
            validated_params[param_name] = get_rqst_params[param_name]


def validate_get_rqst_parameter_phone_number(get_rqst_params, validated_params, rqst_errors):
    param_name = 'phone_number'

    if param_name in get_rqst_params:
        validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_company_name(get_rqst_params, validated_params, rqst_errors):
    param_name = 'company_name'

    if param_name in get_rqst_params:
        validate_url_encoded_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_full_name(get_rqst_params, validated_params, rqst_errors):
    param_name = 'full_name'

    if param_name in get_rqst_params:
        validate_url_encoded_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors)


def validate_int_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors):
    unvalidated_param_value = get_rqst_params[param_name]

    try:
        validated_param_value = int(unvalidated_param_value)
    except ValueError:
        rqst_errors.append('Invalid {} param value. Value must be a base 10 integer.'.format(param_name))
        return None

    validated_params[param_name] = validated_param_value


def validate_int_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors):
    unvalidated_param_value = get_rqst_params[param_name]

    validated_param_value_list = re.findall("\d+", unvalidated_param_value)
    for indx, element in enumerate(validated_param_value_list):
        validated_param_value_list[indx] = int(element)
    validated_params["{}_{}".format(param_name, "list")] = validated_param_value_list

    if not validated_param_value_list:
        rqst_errors.append('Invalid {}, {}s must be base 10 integers'.format(param_name, param_name))

    number_of_commas = len(re.findall(r",", unvalidated_param_value))
    number_of_parameters_there_should_be = number_of_commas + 1
    if number_of_parameters_there_should_be != len(validated_param_value_list):
        rqst_errors.append(
            'List of {}s is formatted wrong. Values must be base 10 integers separated by commas'.format(param_name))


def validate_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors):
    unvalidated_param_value = get_rqst_params[param_name]

    validated_param_value = unvalidated_param_value

    validated_params[param_name] = validated_param_value


def validate_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors):
    unvalidated_param_value = get_rqst_params[param_name]

    validated_param_value_list = re.findall(r"[@\w. '-]+", unvalidated_param_value)
    validated_params["{}_{}".format(param_name, "list")] = validated_param_value_list

    if not validated_param_value_list:
        rqst_errors.append('Invalid {}, {}s must be ascii encoded strings.'.format(param_name, param_name))

    number_of_commas = len(re.findall(r",", unvalidated_param_value))
    number_of_parameters_there_should_be = number_of_commas + 1
    if number_of_parameters_there_should_be != len(validated_param_value_list):
        rqst_errors.append('List of {}s is formatted wrong. Values must be ascii strings separated by commas'.format(param_name))


def validate_url_encoded_string_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors):
    unvalidated_param_value = get_rqst_params[param_name]

    validated_param_value = urllib.parse.unquote(unvalidated_param_value)

    validated_params[param_name] = validated_param_value


def validate_url_encoded_string_list_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors):
    unvalidated_param_value = get_rqst_params[param_name]
    url_decoded_param_value = urllib.parse.unquote(unvalidated_param_value)

    validated_param_value_list = re.findall(r"[@\w. '-]+", url_decoded_param_value)
    validated_params["{}_{}".format(param_name, "list")] = validated_param_value_list

    error_message = 'Comma separated list of {}s is formatted wrong. Values must be ascii strings that have all non-ascii characters url encoded.'.format(param_name)
    if not validated_param_value_list:
        rqst_errors.append(error_message)

    number_of_commas = len(re.findall(r",", unvalidated_param_value))
    number_of_parameters_there_should_be = number_of_commas + 1
    if number_of_parameters_there_should_be != len(validated_param_value_list):
        rqst_errors.append(error_message)


def validate_bool_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors):
    accepted_unvalidated_values = (
        'true',
        'false'
    )

    unvalidated_values_that_equal_true = (
        'true'
    )

    unvalidated_param_value = get_rqst_params[param_name].lower()
    if unvalidated_param_value not in accepted_unvalidated_values:
        rqst_errors.append("Value for {} is not type boolean".format(param_name))

    validated_param_value = unvalidated_param_value in unvalidated_values_that_equal_true
    validated_params[param_name] = validated_param_value


def validate_yyyy_mm_dd_timestamp_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors):
    unvalidated_param_value = get_rqst_params[param_name]

    try:
        validated_param_value = datetime.datetime.strptime(unvalidated_param_value, '%Y-%m-%d')
    except ValueError:
        rqst_errors.append('{} parameter value must be a valid date formatted like: YYYY-MM-DD.'.format(param_name))
        validated_param_value = None

    validated_params[param_name] = validated_param_value


def validate_time_delta_in_days_get_rqst_param(get_rqst_params, validated_params, param_name, rqst_errors):
    unvalidated_param_value = get_rqst_params[param_name]

    try:
        validated_param_value = int(unvalidated_param_value)
    except ValueError:
        rqst_errors.append('Invalid {} param value. Value must be a base 10 integer.'.format(param_name))
        validated_param_value = None
    else:
        validated_param_value = datetime.timedelta(days=validated_param_value)

    validated_params[param_name] = validated_param_value


class HTTPParamValidatorBase:
    param_name = None
    param_types = None
    accepted_param_types = [
        'int',
        'int_list'
        'str',
        'url_encoded_str'
    ]
    is_list_of_params = None

    @classmethod
    def check_that_instance_attributes_are_init(cls):
        if cls.param_name is None:
            raise NotImplementedError("cls.param_name must be set to a non null value in order to use this function.")
        if cls.param_types is None:
            raise NotImplementedError("cls.param_types must be set to a non null value in order to use this function.")
        elif not isinstance(cls.param_types, list):
            raise NotImplementedError("cls.param_types must be set to a list whose values are in: {} in order to use this function.".format(json.dumps(cls.accepted_param_types)))
        if cls.is_list_of_params is None:
            raise NotImplementedError(
                "cls.is_list_of_params must be set to a non null value in order to use this function.")

    @classmethod
    def validate_get_rqst_parameter(cls, get_rqst_params, validated_params, rqst_errors):
        cls.check_that_instance_attributes_are_init()

        for param_type in cls.param_types:
            if param_type == 'int':
                if cls.param_name in get_rqst_params:
                    validate_int_get_rqst_param(get_rqst_params, validated_params, cls.param_name, rqst_errors)

                    validated_param_value = validated_params[cls.param_name]
                    if cls.is_list_of_params and validated_param_value != "all":
                        validate_int_list_get_rqst_param(get_rqst_params, validated_params, cls.param_name, rqst_errors)
            elif param_type == 'int_list':
                if cls.param_name in get_rqst_params:
                    unvalidated_param_value = get_rqst_params[cls.param_name]
                    if unvalidated_param_value != "all":
                        validate_int_list_get_rqst_param(get_rqst_params, validated_params, cls.param_name, rqst_errors)
            elif param_type == 'str':
                if cls.param_name in get_rqst_params:
                    validate_string_get_rqst_param(get_rqst_params, validated_params, cls.param_name, rqst_errors)
            elif param_type == 'url_encoded_str':
                pass
            else:
                raise NotImplementedError("param_type: {} must be in this set of accepted values {}.".format(param_type, json.dumps(cls.accepted_param_types)))


GET_PARAMETER_VALIDATION_FUNCTIONS = {
    "id": {
        'function': validate_get_rqst_parameter_id,
        'type': 'int_with_all'
    },

    "cm_client_id": {
        'function': validate_get_rqst_parameter_cm_client_id,
        'type': 'int_with_all_and_none'
    },
    "cm_sequence_id": {
        'function': validate_get_rqst_parameter_cm_sequence_id,
        'type': 'int_with_all_and_none'
    },

    "nav_id": {
        'function': validate_get_rqst_parameter_nav_id,
        'type': 'int'
    },
    "staff_id": {
        'function': validate_get_rqst_parameter_staff_id,
        'type': 'int'
    },
    "consumer_id": {
        'function': validate_get_rqst_parameter_consumer_id,
        'type': 'int'
    },
    "referring_cm_client_id": {
        'function': validate_get_rqst_parameter_referring_cm_client_id,
        'type': 'int'
    },
    "approved_cm_client_id": {
        'function': validate_get_rqst_parameter_approved_cm_client_id,
        'type': 'int'
    },
    "location_id": {
        'function': validate_get_rqst_parameter_locationid,
        'type': 'int'
    },
    "carrier_id": {
        'function': validate_get_rqst_parameter_carrier_id,
        'type': 'int'
    },
    'accepted_location_id': {
        'function': validate_get_rqst_parameter_accepted_location_id,
        'type': 'int'
    },
    "gen_concern_id": {
        'function': validate_get_rqst_parameter_gen_concern_id,
        'type': 'int'
    },
    "gen_concern_id_subset": {
        'function': validate_get_rqst_parameter_gen_concern_id_subset,
        'type': 'int'
    },
    "family_size": {
        'function': validate_get_rqst_parameter_family_size,
        'type': 'int'
    },
    "network_id": {
        'function': validate_get_rqst_parameter_network_id,
        'type': 'int'
    },
    "partner_id": {
        'function': validate_get_rqst_parameter_partner_id,
        'type': 'int'
    },
    "zipcode": {
        'function': validate_get_rqst_parameter_zipcode,
        'type': 'int'
    },

    "time_delta_in_days": {
        'function': validate_get_rqst_parameter_time_delta_in_days,
        'type': 'time_delta_in_days'
    },
    "page": {
        'function': validate_get_rqst_parameter_page,
        'type': 'single_int'
    },

    "first_name": {
        'function': validate_get_rqst_parameter_first_name,
        'type': 'string'
    },
    "last_name": {
        'function': validate_get_rqst_parameter_last_name,
        'type': 'string'
    },
    "email": {
        'function': validate_get_rqst_parameter_email,
        'type': 'string'
    },
    "mpn": {
        'function': validate_get_rqst_parameter_mpn,
        'type': 'string'
    },
    "region": {
        'function': validate_get_rqst_parameter_region,
        'type': 'string'
    },
    "nav_location_tags": {
        'function': validate_get_rqst_parameter_nav_location_tags,
        'type': 'string'
    },
    "county": {
        'function': validate_get_rqst_parameter_county,
        'type': 'string'
    },
    "state": {
        'function': validate_get_rqst_parameter_state,
        'type': 'string'
    },
    "carrier_state": {
        'function': validate_get_rqst_parameter_carrier_state,
        'type': 'string'
    },
    "premium_type": {
        'function': validate_get_rqst_parameter_premium_type,
        'type': 'string'
    },
    "group_by": {
        'function': validate_get_rqst_parameter_group_by,
        'type': 'string'
    },
    "phone_number": {
        'function': validate_get_rqst_parameter_phone_number,
        'type': 'string'
    },

    "severity": {
        'function': validate_get_rqst_parameter_severity,
        'type': 'url_encoded_string'
    },
    "location": {
        'function': validate_get_rqst_parameter_location,
        'type': 'url_encoded_string'
    },
    "intent": {
        'function': validate_get_rqst_parameter_intent,
        'type': 'url_encoded_string'
    },
    "status": {
        'function': validate_get_rqst_parameter_status,
        'type': 'url_encoded_string'
    },
    "contact_type": {
        'function': validate_get_rqst_parameter_contact_type,
        'type': 'url_encoded_string'
    },
    "carrier_name": {
        'function': validate_get_rqst_parameter_carrier_name,
        'type': 'url_encoded_string'
    },
    "network_name": {
        'function': validate_get_rqst_parameter_network_name,
        'type': 'url_encoded_string'
    },
    "gen_concern_name": {
        'function': validate_get_rqst_parameter_gen_concern_name,
        'type': 'url_encoded_string'
    },
    "hospital_name": {
        'function': validate_get_rqst_parameter_hospital_name,
        'type': 'url_encoded_string'
    },
    'fields': {
        'function': validate_get_rqst_parameter_fields,
        'type': 'url_encoded_string'
    },
    "company_name": {
        'function': validate_get_rqst_parameter_company_name,
        'type': 'url_encoded_string'
    },
    'full_name': {
        'function': validate_get_rqst_parameter_full_name,
        'type': 'url_encoded_string'
    },
    "question": {
        'function': validate_get_rqst_parameter_question,
        'type': 'url_encoded_string'
    },
    "name": {
        'function': validate_get_rqst_parameter_name,
        'type': 'url_encoded_string'
    },
    "user_name": {
        'function': validate_get_rqst_parameter_user_name,
        'type': 'url_encoded_string'
    },
    "tracking_no": {
        'function': validate_get_rqst_parameter_tracking_no,
        'type': 'url_encoded_string'
    },

    "start_date": {
        'function': validate_get_rqst_parameter_start_date,
        'type': 'date_string'
    },
    "end_date": {
        'function': validate_get_rqst_parameter_end_date,
        'type': 'date_string'
    },
    "date_created_start": {
        'function': validate_get_rqst_parameter_date_created_start,
        'type': 'date_string'
    },
    "date_created_end": {
        'function': validate_get_rqst_parameter_date_created_end,
        'type': 'date_string'
    },
    "date_modified_start": {
        'function': validate_get_rqst_parameter_date_modified_start,
        'type': 'date_string'
    },
    "date_modified_end": {
        'function': validate_get_rqst_parameter_date_modified_end,
        'type': 'date_string'
    },
    "datetime_contacted_start_date": {
        'function': validate_get_rqst_parameter_datetime_contacted_start_date,
        'type': 'date_string'
    },
    "datetime_contacted_end_date": {
        'function': validate_get_rqst_parameter_datetime_contacted_end_date,
        'type': 'date_string'
    },
    "datetime_completed_start_date": {
        'function': validate_get_rqst_parameter_datetime_completed_start_date,
        'type': 'date_string'
    },
    "datetime_completed_end_date": {
        'function': validate_get_rqst_parameter_datetime_completed_end_date,
        'type': 'date_string'
    },

    "is_cps_consumer": {
        'function': validate_get_rqst_parameter_is_cps_consumer,
        'type': 'bool_string'
    },
    "is_cps_location": {
        'function': validate_get_rqst_parameter_is_cps_location,
        'type': 'bool_string'
    },
    "has_hospital_info": {
        'function': validate_get_rqst_parameter_has_hospital_info,
        'type': 'bool_string'
    },
    "has_sample_id_card": {
        'function': validate_get_rqst_parameter_has_sample_id_card,
        'type': 'bool_string'
    },
    "include_summary_report": {
        'function': validate_get_rqst_parameter_include_summary_report,
        'type': 'bool_string'
    },
    "include_detailed_report": {
        'function': validate_get_rqst_parameter_include_detailed_report,
        'type': 'bool_string'
    },
}
