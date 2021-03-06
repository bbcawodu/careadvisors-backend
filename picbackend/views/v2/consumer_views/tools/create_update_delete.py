"""
Defines utility functions and classes for consumer views
"""

import datetime
import pytz
import json

from django import forms
from django.core.validators import validate_email
from django.db import IntegrityError

from picbackend.views.utils import clean_bool_value_from_dict_object
from picbackend.views.utils import clean_dict_value_from_dict_object
from picbackend.views.utils import clean_float_value_from_dict_object
from picbackend.views.utils import clean_int_value_from_dict_object
from picbackend.views.utils import clean_list_value_from_dict_object
from picbackend.views.utils import clean_string_value_from_dict_object
from picmodels.models import PICConsumer
from picmodels.models import Navigators
from picmodels.models import CaseManagementStatus
from picmodels.models import CaseManagementClient


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
        validated_params['create_backup'] = clean_bool_value_from_dict_object(
            rqst_body,
            "root",
            "create_backup",
            rqst_errors,
            no_key_allowed=True
        )

    return validated_params


def validate_create_row_params(rqst_body, validated_params, rqst_errors):
    email = clean_string_value_from_dict_object(
        rqst_body,
        "root",
        "email",
        rqst_errors,
        empty_string_allowed=True
    )
    if email and not rqst_errors:
        try:
            validate_email(email)
        except forms.ValidationError:
            rqst_errors.append("{!s} must be a valid email address".format(email))
    validated_params["email"] = email

    first_name = clean_string_value_from_dict_object(rqst_body, "root", "first_name", rqst_errors)
    validated_params["first_name"] = first_name

    middle_name = clean_string_value_from_dict_object(
        rqst_body,
        "root",
        "middle_name",
        rqst_errors,
        empty_string_allowed=True
    )
    validated_params["middle_name"] = middle_name

    last_name = clean_string_value_from_dict_object(rqst_body, "root", "last_name", rqst_errors)
    validated_params["last_name"] = last_name

    if 'gender' in rqst_body:
        validated_params['gender'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            'gender',
            rqst_errors,
            empty_string_allowed=True
        )
        if validated_params['gender'] == '':
            validated_params['gender'] = 'not available'

    if "dob" in rqst_body:
        dob = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "dob",
            rqst_errors,
            none_allowed=True
        )
        validated_dob = None
        if dob:
            try:
                validated_dob = datetime.datetime.strptime(dob, "%Y-%m-%d").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'dob must be a properly formatted date string, eg. YYYY-MM-DD. Value is : {}'.format(
                        dob
                    )
                )
        validated_params['dob'] = validated_dob

    if 'referral_channel' in rqst_body:
        validated_params['referral_channel'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            'referral_channel',
            rqst_errors,
            empty_string_allowed=True
        )
        if validated_params['referral_channel'] == '':
            validated_params['referral_channel'] = 'not available'
    if 'referral_type' in rqst_body:
        validated_params['referral_type'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            'referral_type',
            rqst_errors,
            none_allowed=True
        )

    plan = clean_string_value_from_dict_object(
        rqst_body,
        "root",
        "plan",
        rqst_errors,
        empty_string_allowed=True,
        none_allowed=True
    )
    validated_params["plan"] = plan

    met_nav_at = clean_string_value_from_dict_object(rqst_body, "root", "met_nav_at", rqst_errors)
    validated_params["met_nav_at"] = met_nav_at

    household_size = clean_int_value_from_dict_object(rqst_body, "root", "household_size", rqst_errors, none_allowed=True)
    validated_params["household_size"] = household_size

    phone = clean_string_value_from_dict_object(
        rqst_body,
        "root",
        "phone",
        rqst_errors,
        empty_string_allowed=True
    )
    validated_params["phone"] = phone

    preferred_language = clean_string_value_from_dict_object(
        rqst_body,
        "root",
        "preferred_language",
        rqst_errors,
        empty_string_allowed=True
    )
    validated_params["preferred_language"] = preferred_language

    best_contact_time = clean_string_value_from_dict_object(
        rqst_body,
        "root",
        "best_contact_time",
        rqst_errors,
        no_key_allowed=True,
        empty_string_allowed=True
    )
    validated_params['best_contact_time'] = best_contact_time

    consumer_notes = clean_list_value_from_dict_object(
        rqst_body,
        "root",
        "consumer_notes",
        rqst_errors,
        empty_list_allowed=True
    )
    validated_params["consumer_notes"] = consumer_notes

    address_line_1 = clean_string_value_from_dict_object(
        rqst_body,
        "root",
        "address_line_1",
        rqst_errors,
        empty_string_allowed=True
    )
    validated_params["address_line_1"] = address_line_1

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

    city = clean_string_value_from_dict_object(rqst_body, "root", "city", rqst_errors, empty_string_allowed=True)
    validated_params["city"] = city

    state_province = clean_string_value_from_dict_object(
        rqst_body,
        "root",
        "state_province",
        rqst_errors,
        empty_string_allowed=True
    )
    validated_params["state_province"] = state_province

    zipcode = clean_string_value_from_dict_object(
        rqst_body,
        "root",
        "zipcode",
        rqst_errors,
        empty_string_allowed=True
    )
    validated_params["zipcode"] = zipcode

    validated_params['force_create_consumer'] = clean_bool_value_from_dict_object(rqst_body,
                                                                                  "root",
                                                                                  "force_create_consumer",
                                                                                  rqst_errors,
                                                                                  no_key_allowed=True)

    date_met_nav_dict = clean_dict_value_from_dict_object(
        rqst_body,
        "root",
        "date_met_nav",
        rqst_errors,
        none_allowed=True
    )
    date_met_nav = None
    if date_met_nav_dict is not None:
        month = clean_int_value_from_dict_object(date_met_nav_dict, "date_met_nav", "Month", rqst_errors)
        if month:
            if month < 1 or month > 12:
                rqst_errors.append("Month must be between 1 and 12 inclusive")

        day = clean_int_value_from_dict_object(date_met_nav_dict, "date_met_nav", "Day", rqst_errors)
        if day:
            if day < 1 or day > 31:
                rqst_errors.append("Day must be between 1 and 31 inclusive")

        year = clean_int_value_from_dict_object(date_met_nav_dict, "date_met_nav", "Year", rqst_errors)
        if year:
            if year < 1 or year > 9999:
                rqst_errors.append("Year must be between 1 and 9999 inclusive")

        if not rqst_errors:
            date_met_nav = datetime.date(year, month, day)
    validated_params["date_met_nav"] = date_met_nav

    if "datetime_received_by_client" in rqst_body:
        datetime_received_by_client = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "datetime_received_by_client",
            rqst_errors,
            none_allowed=True
        )
        validated_datetime_received_by_client = None
        if datetime_received_by_client:
            try:
                validated_datetime_received_by_client = datetime.datetime.strptime(datetime_received_by_client, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'datetime_received_by_client must be a properly formatted datetime string in UTC, eg. YYYY-MM-DDTHH:MM:SS. Value is : {}'.format(
                        datetime_received_by_client)
                )
        validated_params['datetime_received_by_client'] = validated_datetime_received_by_client

    navigator_row = None
    if "navigator_id" in rqst_body:
        navigator_id = clean_int_value_from_dict_object(rqst_body, "root", "navigator_id", rqst_errors, none_allowed=True)
        if navigator_id:
            try:
                navigator_row = Navigators.objects.get(id=navigator_id)
            except Navigators.DoesNotExist:
                rqst_errors.append('Staff database entry does not exist for the navigator id: {}'.format(navigator_id))
        validated_params["navigator_id"] = navigator_id
        validated_params["navigator_row"] = navigator_row

    cm_client_row_for_routing = None
    if "cm_client_id_for_routing" in rqst_body:
        cm_client_id_for_routing = clean_int_value_from_dict_object(
            rqst_body,
            "root",
            "cm_client_id_for_routing",
            rqst_errors,
            none_allowed=True
        )
        if cm_client_id_for_routing:
            try:
                cm_client_row_for_routing = CaseManagementClient.objects.get(id=cm_client_id_for_routing)
            except CaseManagementClient.DoesNotExist:
                rqst_errors.append(
                    'Row does not exist in CaseManagementClient Table for the cm_client_id_for_routing: {}'.format(
                        cm_client_id_for_routing
                    )
                )
        validated_params["cm_client_id_for_routing"] = cm_client_id_for_routing
        validated_params["cm_client_row_for_routing"] = cm_client_row_for_routing

    if not ((navigator_row != None) ^ (cm_client_row_for_routing != None)):
        rqst_errors.append("Valid navigator logical exclusive or case_management_client_for_roouting must be given for consumer assignment.")

    if 'add_referring_cm_clients' in rqst_body:
        add_referring_cm_clients = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "add_referring_cm_clients",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_referring_cm_clients = []
        for referring_cm_client in add_referring_cm_clients:
            if not isinstance(referring_cm_client, int):
                rqst_errors.append('Error: A referring_cm_client in \'add_referring_cm_clients\' is not an integer.')
                continue

            validated_referring_cm_clients.append(referring_cm_client)

        validated_params['add_referring_cm_clients'] = validated_referring_cm_clients

    cps_info_dict = clean_dict_value_from_dict_object(rqst_body,
                                                           "root",
                                                           "cps_info",
                                                           rqst_errors,
                                                           no_key_allowed=True,
                                                           none_allowed=True)
    validated_cps_info_dict = None
    if cps_info_dict and navigator_row:
        validated_cps_info_dict = validate_cps_info_params_for_add_instance_rqst(cps_info_dict, met_nav_at, household_size, navigator_row, rqst_errors)
    validated_params["cps_info_dict"] = cps_info_dict
    validated_params["validated_cps_info_dict"] = validated_cps_info_dict

    create_backup = clean_bool_value_from_dict_object(rqst_body,
                                                           "root",
                                                           "create_backup",
                                                           rqst_errors,
                                                           no_key_allowed=True)
    validated_params["create_backup"] = create_backup

    validate_consumer_hospital_data_params(rqst_body, validated_params, rqst_errors)
    validate_consumer_payer_data_params(rqst_body, validated_params, rqst_errors)

    if "create_case_management_rows" in rqst_body:
        rqst_case_management_row_data = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "create_case_management_rows",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_create_c_m_params = []
        if rqst_case_management_row_data:
            for rqst_case_row_index, rqst_case_management_dict in enumerate(rqst_case_management_row_data):
                validated_c_m_row_params = validate_create_c_m_status_data(
                    rqst_case_management_dict,
                    rqst_case_row_index,
                    validated_params,
                    rqst_errors
                )
                validated_create_c_m_params.append(validated_c_m_row_params)

        validated_params['validated_create_c_m_params'] = validated_create_c_m_params

    validate_indiv_seeking_nav_params(rqst_body, validated_params, rqst_errors)


def validate_update_row_params(rqst_body, validated_params, rqst_errors):
    consumer_instance = None
    rqst_id = validated_params['id']
    if not rqst_errors:
        try:
            consumer_instance = PICConsumer.objects.get(id=rqst_id)
        except PICConsumer.DoesNotExist:
            rqst_errors.append('Consumer database entry does not exist for the id: {}'.format(rqst_id))
    validated_params['consumer_instance'] = consumer_instance

    if "email" in rqst_body:
        email = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "email",
            rqst_errors,
            empty_string_allowed=True
        )
        if email:
            try:
                validate_email(email)
            except forms.ValidationError:
                rqst_errors.append("{!s} must be a valid email address".format(email))

        validated_params["email"] = email

    if "first_name" in rqst_body:
        first_name = clean_string_value_from_dict_object(rqst_body, "root", "first_name", rqst_errors)

        validated_params["first_name"] = first_name

    if "middle_name" in rqst_body:
        middle_name = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "middle_name",
            rqst_errors,
            empty_string_allowed=True
        )

        validated_params["middle_name"] = middle_name

    if "last_name" in rqst_body:
        last_name = clean_string_value_from_dict_object(rqst_body, "root", "last_name", rqst_errors)

        validated_params["last_name"] = last_name

    if 'gender' in rqst_body:
        validated_params['gender'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            'gender',
            rqst_errors,
            empty_string_allowed=True
        )
        if validated_params['gender'] == '':
            validated_params['gender'] = 'not available'

    if "dob" in rqst_body:
        dob = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "dob",
            rqst_errors,
            none_allowed=True
        )
        validated_dob = None
        if dob:
            try:
                validated_dob = datetime.datetime.strptime(dob, "%Y-%m-%d").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'dob must be a properly formatted date string, eg. YYYY-MM-DD. Value is : {}'.format(
                        dob
                    )
                )
        validated_params['dob'] = validated_dob

    if 'referral_channel' in rqst_body:
        validated_params['referral_channel'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            'referral_channel',
            rqst_errors,
            empty_string_allowed=True
        )
        if validated_params['referral_channel'] == '':
            validated_params['referral_channel'] = 'not available'

    if 'referral_type' in rqst_body:
        validated_params['referral_type'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            'referral_type',
            rqst_errors,
            none_allowed=True
        )

    if "plan" in rqst_body:
        plan = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "plan",
            rqst_errors,
            empty_string_allowed=True
        )

        validated_params["plan"] = plan

    met_nav_at = None
    if "met_nav_at" in rqst_body:
        met_nav_at = clean_string_value_from_dict_object(rqst_body, "root", "met_nav_at", rqst_errors)

        validated_params["met_nav_at"] = met_nav_at

    household_size = None
    if "household_size" in rqst_body:
        household_size = clean_int_value_from_dict_object(rqst_body, "root", "household_size", rqst_errors, none_allowed=True)

        validated_params["household_size"] = household_size

    if "phone" in rqst_body:
        phone = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "phone",
            rqst_errors,
            empty_string_allowed=True
        )

        validated_params["phone"] = phone

    if "preferred_language" in rqst_body:
        preferred_language = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "preferred_language",
            rqst_errors,
            empty_string_allowed=True
        )

        validated_params["preferred_language"] = preferred_language

    if "best_contact_time" in rqst_body:
        best_contact_time = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "best_contact_time",
            rqst_errors,
            empty_string_allowed=True
        )
        validated_params["best_contact_time"] = best_contact_time

    if "consumer_notes" in rqst_body:
        consumer_notes = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "consumer_notes",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_params["consumer_notes"] = consumer_notes

    validate_consumer_hospital_data_params(rqst_body, validated_params, rqst_errors)
    validate_consumer_payer_data_params(rqst_body, validated_params, rqst_errors)

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
        city = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "city",
            rqst_errors,
            empty_string_allowed=True
        )

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

    navigator_row = None
    if "navigator_id" in rqst_body:
        navigator_id = clean_int_value_from_dict_object(rqst_body, "root", "navigator_id", rqst_errors, none_allowed=True)
        if navigator_id and not rqst_errors:
            try:
                navigator_row = Navigators.objects.get(id=navigator_id)
            except Navigators.DoesNotExist:
                rqst_errors.append('Staff database entry does not exist for the navigator id: {}'.format(navigator_id))

        validated_params["navigator_id"] = navigator_id
        validated_params["navigator_row"] = navigator_row

    cm_client_row_for_routing = None
    if "cm_client_id_for_routing" in rqst_body:
        cm_client_id_for_routing = clean_int_value_from_dict_object(
            rqst_body,
            "root",
            "cm_client_id_for_routing",
            rqst_errors,
            none_allowed=True
        )
        if cm_client_id_for_routing and not rqst_errors:
            try:
                cm_client_row_for_routing = CaseManagementClient.objects.get(id=cm_client_id_for_routing)
            except CaseManagementClient.DoesNotExist:
                rqst_errors.append(
                    'Row does not exist in CaseManagementClient Table for the cm_client_id_for_routing: {}'.format(
                        cm_client_id_for_routing
                    )
                )
        validated_params["cm_client_id_for_routing"] = cm_client_id_for_routing
        validated_params["cm_client_row_for_routing"] = cm_client_row_for_routing

    if navigator_row and cm_client_row_for_routing:
        rqst_errors.append("Valid navigator and case_management_client_for_roouting can not be given at the same time for consumer assignment.")

    if 'add_referring_cm_clients' in rqst_body:
        add_referring_cm_clients = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "add_referring_cm_clients",
            rqst_errors
        )

        validated_referring_cm_clients = []
        for referring_cm_client in add_referring_cm_clients:
            if not isinstance(referring_cm_client, int):
                rqst_errors.append('Error: A referring_cm_client in \'add_referring_cm_clients\' is not an integer.')
                continue

            validated_referring_cm_clients.append(referring_cm_client)

        validated_params['add_referring_cm_clients'] = validated_referring_cm_clients
    elif 'remove_referring_cm_clients' in rqst_body:
        remove_referring_cm_clients = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "remove_referring_cm_clients",
            rqst_errors
        )

        validated_referring_cm_clients = []
        for referring_cm_client in remove_referring_cm_clients:
            if not isinstance(referring_cm_client, int):
                rqst_errors.append('Error: A referring_cm_client in \'remove_referring_cm_clients\' is not an integer.')
                continue

            validated_referring_cm_clients.append(referring_cm_client)

        validated_params['remove_referring_cm_clients'] = validated_referring_cm_clients

    date_met_nav = None
    if "date_met_nav" in rqst_body:
        date_met_nav_dict = clean_dict_value_from_dict_object(rqst_body, "root", "date_met_nav", rqst_errors,
                                                              none_allowed=True)
        if date_met_nav_dict is not None:
            month = clean_int_value_from_dict_object(date_met_nav_dict, "date_met_nav", "Month", rqst_errors)
            if month:
                if month < 1 or month > 12:
                    rqst_errors.append("Month must be between 1 and 12 inclusive")

            day = clean_int_value_from_dict_object(date_met_nav_dict, "date_met_nav", "Day", rqst_errors)
            if day:
                if day < 1 or day > 31:
                    rqst_errors.append("Day must be between 1 and 31 inclusive")

            year = clean_int_value_from_dict_object(date_met_nav_dict, "date_met_nav", "Year", rqst_errors)
            if year:
                if year < 1 or year > 9999:
                    rqst_errors.append("Year must be between 1 and 9999 inclusive")

            if not rqst_errors:
                date_met_nav = datetime.date(year, month, day)

        validated_params["date_met_nav"] = date_met_nav

    if "datetime_received_by_client" in rqst_body:
        datetime_received_by_client = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "datetime_received_by_client",
            rqst_errors,
            none_allowed=True
        )
        validated_datetime_received_by_client = None
        if datetime_received_by_client:
            try:
                validated_datetime_received_by_client = datetime.datetime.strptime(datetime_received_by_client, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'datetime_received_by_client must be a properly formatted datetime string in UTC, eg. YYYY-MM-DDTHH:MM:SS. Value is : {}'.format(
                        datetime_received_by_client)
                )
        validated_params['datetime_received_by_client'] = validated_datetime_received_by_client

    if "cps_info" in rqst_body:
        cps_info_dict = clean_dict_value_from_dict_object(rqst_body,
                                                               "root",
                                                               "cps_info",
                                                               rqst_errors,
                                                               none_allowed=True)
        validated_cps_info_dict = None
        if consumer_instance and cps_info_dict:
            validated_cps_info_dict = validate_cps_info_params_for_modify_instance_rqst(
                cps_info_dict,
                consumer_instance,
                met_nav_at,
                household_size,
                navigator_row,
                rqst_errors
            )

        validated_params["cps_info_dict"] = cps_info_dict
        validated_params["validated_cps_info_dict"] = validated_cps_info_dict

    if "create_backup" in rqst_body:
        validated_params['create_backup'] = clean_bool_value_from_dict_object(rqst_body,
                                                                                   "root",
                                                                                   "create_backup",
                                                                                   rqst_errors,
                                                                                   no_key_allowed=True)

    if "create_case_management_rows" in rqst_body:
        rqst_case_management_row_data = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "create_case_management_rows",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_create_c_m_params = []
        if rqst_case_management_row_data:
            for rqst_case_row_index, rqst_case_management_dict in enumerate(rqst_case_management_row_data):
                validated_c_m_row_params = validate_create_c_m_status_data(
                    rqst_case_management_dict,
                    rqst_case_row_index,
                    validated_params,
                    rqst_errors
                )
                validated_create_c_m_params.append(validated_c_m_row_params)

        validated_params['validated_create_c_m_params'] = validated_create_c_m_params
    elif "update_case_management_rows" in rqst_body:
        rqst_case_management_row_data = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "update_case_management_rows",
            rqst_errors
        )

        validated_update_c_m_params = []
        if rqst_case_management_row_data:
            for rqst_case_row_index, rqst_case_management_dict in enumerate(rqst_case_management_row_data):
                validated_c_m_row_params = validate_update_c_m_status_data(
                    rqst_case_management_dict,
                    rqst_case_row_index,
                    rqst_errors
                )
                validated_update_c_m_params.append(validated_c_m_row_params)

        validated_params['validated_update_c_m_params'] = validated_update_c_m_params
    elif "delete_case_management_rows" in rqst_body:
        rqst_case_management_row_data = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "delete_case_management_rows",
            rqst_errors
        )

        validated_delete_c_m_params = []
        if rqst_case_management_row_data:
            for rqst_c_m_id in rqst_case_management_row_data:
                validated_c_m_row_params = validate_delete_c_m_status_data(
                    rqst_c_m_id,
                    rqst_errors
                )
                validated_delete_c_m_params.append(validated_c_m_row_params)

        validated_params['validated_delete_c_m_params'] = validated_delete_c_m_params

    validate_indiv_seeking_nav_params(rqst_body, validated_params, rqst_errors)

    if len(validated_params) < 3 or "id" not in validated_params:
        rqst_errors.append("No parameters to modify are given.")


def validate_consumer_hospital_data_params(rqst_body, validated_params, rqst_errors):
    if "create_consumer_hospital_data_rows" in rqst_body:
        rqst_consumer_hospital_data_row_data = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "create_consumer_hospital_data_rows",
            rqst_errors
        )

        validated_create_consumer_hospital_data_params = []
        if rqst_consumer_hospital_data_row_data:
            for rqst_consumer_hospital_data_row_index, rqst_consumer_hospital_data_dict in enumerate(rqst_consumer_hospital_data_row_data):
                validated_consumer_hospital_data_row_params = validate_create_consumer_hospital_data_params(
                    rqst_consumer_hospital_data_dict,
                    rqst_consumer_hospital_data_row_index,
                    rqst_errors
                )
                validated_create_consumer_hospital_data_params.append(validated_consumer_hospital_data_row_params)

        validated_params['create_consumer_hospital_data_rows'] = validated_create_consumer_hospital_data_params
    elif "update_consumer_hospital_data_rows" in rqst_body:
        rqst_consumer_hospital_data_row_data = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "update_consumer_hospital_data_rows",
            rqst_errors
        )

        validated_update_consumer_hospital_data_params = []
        if rqst_consumer_hospital_data_row_data:
            for rqst_consumer_hospital_data_row_index, rqst_consumer_hospital_data_dict in enumerate(rqst_consumer_hospital_data_row_data):
                validated_consumer_hospital_data_row_params = validate_update_consumer_hospital_data_params(
                    rqst_consumer_hospital_data_dict,
                    rqst_consumer_hospital_data_row_index,
                    rqst_errors
                )
                validated_update_consumer_hospital_data_params.append(validated_consumer_hospital_data_row_params)

        validated_params['update_consumer_hospital_data_rows'] = validated_update_consumer_hospital_data_params
    elif "delete_consumer_hospital_data_rows" in rqst_body:
        rqst_consumer_hospital_data_row_data = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "delete_consumer_hospital_data_rows",
            rqst_errors
        )

        validated_delete_consumer_hospital_data_params = []
        if rqst_consumer_hospital_data_row_data:
            for rqst_consumer_hospital_data_row_index, rqst_consumer_hospital_data_id in enumerate(rqst_consumer_hospital_data_row_data):
                validated_consumer_hospital_data_row_params = validate_delete_consumer_hospital_data_params(
                    rqst_consumer_hospital_data_id,
                    rqst_consumer_hospital_data_row_index,
                    rqst_errors
                )
                validated_delete_consumer_hospital_data_params.append(validated_consumer_hospital_data_row_params)

        validated_params['delete_consumer_hospital_data_rows'] = validated_delete_consumer_hospital_data_params


def validate_create_consumer_hospital_data_params(consumer_hospital_data_dict, consumer_hospital_data_row_index, rqst_errors):
    validated_params = {}

    if 'hospital_name' in consumer_hospital_data_dict:
        validated_params['hospital_name'] = clean_string_value_from_dict_object(
            consumer_hospital_data_dict,
            "create_consumer_hospital_data_rows[{!s}]".format(consumer_hospital_data_row_index),
            "hospital_name",
            rqst_errors
        )

    if 'medical_record_number' in consumer_hospital_data_dict:
        validated_params['medical_record_number'] = clean_string_value_from_dict_object(
            consumer_hospital_data_dict,
            "create_consumer_hospital_data_rows[{!s}]".format(consumer_hospital_data_row_index),
            "medical_record_number",
            rqst_errors
        )

    if 'billing_amount' in consumer_hospital_data_dict:
        validated_params['billing_amount'] = clean_float_value_from_dict_object(
            consumer_hospital_data_dict,
            "create_consumer_hospital_data_rows[{!s}]".format(consumer_hospital_data_row_index),
            'billing_amount',
            rqst_errors,
            none_allowed=True,
        )
        if validated_params['billing_amount'] and validated_params['billing_amount'] < 0:
            rqst_errors.append(
                "Value for 'billing_amount' must be greater than 0. Given value is: {}. create_consumer_hospital_data_row index: {}".format(
                    validated_params['billing_amount'],
                    consumer_hospital_data_row_index
                )
            )

    if "discharge_date" in consumer_hospital_data_dict:
        discharge_date = clean_string_value_from_dict_object(
            consumer_hospital_data_dict,
            "create_consumer_hospital_data_rows[{!s}]".format(consumer_hospital_data_row_index),
            "discharge_date",
            rqst_errors,
            none_allowed=True
        )
        validated_discharge_date = None
        if discharge_date:
            try:
                validated_discharge_date = datetime.datetime.strptime(discharge_date, "%Y-%m-%d").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'discharge_date must be a properly formatted date string, eg. YYYY-MM-DD. Value is : {}. create_consumer_hospital_data index is: {}'.format(
                        discharge_date,
                        consumer_hospital_data_row_index
                    )
                )
        validated_params['discharge_date'] = validated_discharge_date

    return validated_params


def validate_update_consumer_hospital_data_params(consumer_hospital_data_dict, consumer_hospital_data_row_index, rqst_errors):
    validated_params = {}

    validated_params['id'] = clean_int_value_from_dict_object(
        consumer_hospital_data_dict,
        "update_consumer_hospital_data_rows[{!s}]".format(consumer_hospital_data_row_index),
        "id",
        rqst_errors
    )

    if 'hospital_name' in consumer_hospital_data_dict:
        validated_params['hospital_name'] = clean_string_value_from_dict_object(
            consumer_hospital_data_dict,
            "update_consumer_hospital_data_rows[{!s}]".format(consumer_hospital_data_row_index),
            "hospital_name",
            rqst_errors
        )

    if 'medical_record_number' in consumer_hospital_data_dict:
        validated_params['medical_record_number'] = clean_string_value_from_dict_object(
            consumer_hospital_data_dict,
            "update_consumer_hospital_data_rows[{!s}]".format(consumer_hospital_data_row_index),
            "medical_record_number",
            rqst_errors
        )

    if 'billing_amount' in consumer_hospital_data_dict:
        validated_params['billing_amount'] = clean_float_value_from_dict_object(
            consumer_hospital_data_dict,
            "update_consumer_hospital_data_rows[{!s}]".format(consumer_hospital_data_row_index),
            'billing_amount',
            rqst_errors,
            none_allowed=True,
        )
        if validated_params['billing_amount'] and validated_params['billing_amount'] < 0:
            rqst_errors.append(
                "Value for 'billing_amount' must be greater than 0. Given value is: {}. update_consumer_hospital_data_row index: {}".format(
                    validated_params['billing_amount'],
                    consumer_hospital_data_row_index
                )
            )

    if "discharge_date" in consumer_hospital_data_dict:
        discharge_date = clean_string_value_from_dict_object(
            consumer_hospital_data_dict,
            "update_consumer_hospital_data_rows[{!s}]".format(consumer_hospital_data_row_index),
            "discharge_date",
            rqst_errors,
            none_allowed=True
        )
        validated_discharge_date = None
        if discharge_date:
            try:
                validated_discharge_date = datetime.datetime.strptime(discharge_date, "%Y-%m-%d").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'discharge_date must be a properly formatted date string, eg. YYYY-MM-DD. Value is : {}. update_consumer_hospital_data index is: {}'.format(
                        discharge_date,
                        consumer_hospital_data_row_index
                    )
                )
        validated_params['discharge_date'] = validated_discharge_date

    return validated_params


def validate_delete_consumer_hospital_data_params(consumer_hospital_data_id, consumer_hospital_data_row_index, rqst_errors):
    validated_params = {}

    if not isinstance(consumer_hospital_data_id, int):
        rqst_errors.append(
            "id in delete_consumer_hospital_data_row is not an integer at index: {}".format(
                consumer_hospital_data_row_index
            )
        )

        return None

    validated_params['id'] = consumer_hospital_data_id

    return validated_params


def validate_consumer_payer_data_params(rqst_body, validated_params, rqst_errors):
    if "create_consumer_payer_data_rows" in rqst_body:
        rqst_consumer_payer_data_row_data = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "create_consumer_payer_data_rows",
            rqst_errors
        )

        validated_create_consumer_payer_data_params = []
        if rqst_consumer_payer_data_row_data:
            for rqst_consumer_payer_data_row_index, rqst_consumer_payer_data_dict in enumerate(rqst_consumer_payer_data_row_data):
                validated_consumer_payer_data_row_params = validate_create_consumer_payer_data_params(
                    rqst_consumer_payer_data_dict,
                    rqst_consumer_payer_data_row_index,
                    rqst_errors
                )
                validated_create_consumer_payer_data_params.append(validated_consumer_payer_data_row_params)

        validated_params['create_consumer_payer_data_rows'] = validated_create_consumer_payer_data_params
    elif "update_consumer_payer_data_rows" in rqst_body:
        rqst_consumer_payer_data_row_data = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "update_consumer_payer_data_rows",
            rqst_errors
        )

        validated_update_consumer_payer_data_params = []
        if rqst_consumer_payer_data_row_data:
            for rqst_consumer_payer_data_row_index, rqst_consumer_payer_data_dict in enumerate(rqst_consumer_payer_data_row_data):
                validated_consumer_payer_data_row_params = validate_update_consumer_payer_data_params(
                    rqst_consumer_payer_data_dict,
                    rqst_consumer_payer_data_row_index,
                    rqst_errors
                )
                validated_update_consumer_payer_data_params.append(validated_consumer_payer_data_row_params)

        validated_params['update_consumer_payer_data_rows'] = validated_update_consumer_payer_data_params
    elif "delete_consumer_payer_data_rows" in rqst_body:
        rqst_consumer_payer_data_row_data = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "delete_consumer_payer_data_rows",
            rqst_errors
        )

        validated_delete_consumer_payer_data_params = []
        if rqst_consumer_payer_data_row_data:
            for rqst_consumer_payer_data_row_index, rqst_consumer_payer_data_id in enumerate(rqst_consumer_payer_data_row_data):
                validated_consumer_payer_data_row_params = validate_delete_consumer_payer_data_params(
                    rqst_consumer_payer_data_id,
                    rqst_consumer_payer_data_row_index,
                    rqst_errors
                )
                validated_delete_consumer_payer_data_params.append(validated_consumer_payer_data_row_params)

        validated_params['delete_consumer_payer_data_rows'] = validated_delete_consumer_payer_data_params


def validate_create_consumer_payer_data_params(consumer_payer_data_dict, consumer_payer_data_row_index, rqst_errors):
    validated_params = {}

    if 'risk' in consumer_payer_data_dict:
        validated_params['risk'] = clean_string_value_from_dict_object(
            consumer_payer_data_dict,
            "create_consumer_payer_data_rows[{!s}]".format(consumer_payer_data_row_index),
            "risk",
            rqst_errors,
            none_allowed=True
        )

    if 'member_id_number' in consumer_payer_data_dict:
        validated_params['member_id_number'] = clean_string_value_from_dict_object(
            consumer_payer_data_dict,
            "create_consumer_payer_data_rows[{!s}]".format(consumer_payer_data_row_index),
            "member_id_number",
            rqst_errors,
            none_allowed=True
        )

    if "effective_date" in consumer_payer_data_dict:
        effective_date = clean_string_value_from_dict_object(
            consumer_payer_data_dict,
            "create_consumer_payer_data_rows[{!s}]".format(consumer_payer_data_row_index),
            "effective_date",
            rqst_errors,
            none_allowed=True
        )
        validated_effective_date = None
        if effective_date:
            try:
                validated_effective_date = datetime.datetime.strptime(effective_date, "%Y-%m-%d").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'effective_date must be a properly formatted date string, eg. YYYY-MM-DD. Value is : {}. create_consumer_payer_data index is: {}'.format(
                        effective_date,
                        consumer_payer_data_row_index
                    )
                )
        validated_params['effective_date'] = validated_effective_date

    if 'coverage_type' in consumer_payer_data_dict:
        validated_params['coverage_type'] = clean_string_value_from_dict_object(
            consumer_payer_data_dict,
            "create_consumer_payer_data_rows[{!s}]".format(consumer_payer_data_row_index),
            "coverage_type",
            rqst_errors,
            empty_string_allowed=True
        )
        if not rqst_errors and not validated_params['coverage_type']:
            validated_params['coverage_type'] = 'Not Available'

    if 'case_type_id' in consumer_payer_data_dict:
        validated_params['case_type_id'] = clean_int_value_from_dict_object(
            consumer_payer_data_dict,
            "create_consumer_payer_data_rows[{!s}]".format(consumer_payer_data_row_index),
            "case_type_id",
            rqst_errors,
            none_allowed=True
        )

    return validated_params


def validate_update_consumer_payer_data_params(consumer_payer_data_dict, consumer_payer_data_row_index, rqst_errors):
    validated_params = {}

    validated_params['id'] = clean_int_value_from_dict_object(
        consumer_payer_data_dict,
        "update_consumer_payer_data_rows[{!s}]".format(consumer_payer_data_row_index),
        "id",
        rqst_errors
    )

    if 'risk' in consumer_payer_data_dict:
        validated_params['risk'] = clean_string_value_from_dict_object(
            consumer_payer_data_dict,
            "update_consumer_payer_data_rows[{!s}]".format(consumer_payer_data_row_index),
            "risk",
            rqst_errors,
            none_allowed=True
        )

    if 'member_id_number' in consumer_payer_data_dict:
        validated_params['member_id_number'] = clean_string_value_from_dict_object(
            consumer_payer_data_dict,
            "update_consumer_payer_data_rows[{!s}]".format(consumer_payer_data_row_index),
            "member_id_number",
            rqst_errors,
            none_allowed=True
        )

    if "effective_date" in consumer_payer_data_dict:
        effective_date = clean_string_value_from_dict_object(
            consumer_payer_data_dict,
            "update_consumer_payer_data_rows[{!s}]".format(consumer_payer_data_row_index),
            "effective_date",
            rqst_errors,
            none_allowed=True
        )
        validated_effective_date = None
        if effective_date:
            try:
                validated_effective_date = datetime.datetime.strptime(effective_date, "%Y-%m-%d").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'effective_date must be a properly formatted date string, eg. YYYY-MM-DD. Value is : {}. update_consumer_payer_data index is: {}'.format(
                        effective_date,
                        consumer_payer_data_row_index
                    )
                )
        validated_params['effective_date'] = validated_effective_date

    if 'coverage_type' in consumer_payer_data_dict:
        validated_params['coverage_type'] = clean_string_value_from_dict_object(
            consumer_payer_data_dict,
            "update_consumer_payer_data_rows[{!s}]".format(consumer_payer_data_row_index),
            "coverage_type",
            rqst_errors,
            empty_string_allowed=True
        )
        if not rqst_errors and not validated_params['coverage_type']:
            validated_params['coverage_type'] = 'Not Available'

    if 'case_type_id' in consumer_payer_data_dict:
        validated_params['case_type_id'] = clean_int_value_from_dict_object(
            consumer_payer_data_dict,
            "update_consumer_payer_data_rows[{!s}]".format(consumer_payer_data_row_index),
            "case_type_id",
            rqst_errors,
            none_allowed=True
        )

    return validated_params


def validate_delete_consumer_payer_data_params(consumer_payer_data_id, consumer_payer_data_row_index, rqst_errors):
    validated_params = {}

    if not isinstance(consumer_payer_data_id, int):
        rqst_errors.append(
            "id in delete_consumer_payer_data_row is not an integer at index: {}".format(
                consumer_payer_data_row_index
            )
        )

        return None

    validated_params['id'] = consumer_payer_data_id

    return validated_params


def validate_create_c_m_status_data(rqst_case_management_dict, rqst_case_row_index, validated_params, rqst_errors):
    validated_c_m_row_params = {

    }
    rqst_management_step = clean_int_value_from_dict_object(rqst_case_management_dict,
                                                            "create_case_management_rows[{!s}]".format(rqst_case_row_index),
                                                            "management_step",
                                                            rqst_errors
                                                            )
    if rqst_management_step:
        if rqst_management_step > 9:
            rqst_errors.append(
                "management_step for create_case_management_rows[{!s}] must be < 9".format(
                    rqst_case_row_index))
    validated_c_m_row_params['rqst_management_step'] = rqst_management_step

    rqst_management_notes = clean_string_value_from_dict_object(rqst_case_management_dict,
                                                                "create_case_management_rows[{!s}]".format(
                                                                    rqst_case_row_index),
                                                                "management_notes",
                                                                rqst_errors,
                                                                empty_string_allowed=True
                                                                )
    validated_c_m_row_params['rqst_management_notes'] = rqst_management_notes

    if "id" in validated_params and not rqst_errors:
        matching_c_m_steps = CaseManagementStatus.objects.all().filter(
            management_step=rqst_management_step,
            contact=validated_params["id"]
        ).values_list('id', flat=True)

        if len(matching_c_m_steps):
            rqst_errors.append(
                "case_management_rows with matching management_steps already exist for create_case_management_rows. matching ids: {!s}".format(
                    matching_c_m_steps))

    return validated_c_m_row_params


def validate_update_c_m_status_data(rqst_case_management_dict, rqst_case_row_index, rqst_errors):
    validated_c_m_row_params = {

    }

    rqst_management_status_id = clean_int_value_from_dict_object(rqst_case_management_dict,
                                                                 "create_case_management_rows[{!s}]".format(rqst_case_row_index),
                                                                 "id",
                                                                 rqst_errors
                                                                 )
    validated_c_m_row_params['rqst_management_status_id'] = rqst_management_status_id
    if rqst_management_status_id:
        try:
            case_status_row = CaseManagementStatus.objects.get(id=rqst_management_status_id)
        except CaseManagementStatus.DoesNotExist:
            rqst_errors.append('Case Management Status Row does not exist for the id: {!s}'.format(
                str(rqst_management_status_id)))
        except CaseManagementStatus.MultipleObjectsReturned:
            rqst_errors.append(
                'Multiple Case Management Status Rows exist for the id: {!s}'.format(
                    str(rqst_management_status_id)))
        except IntegrityError:
            rqst_errors.append(
                'Case Management Status Row already exists for the id: {!s}'.format(
                    str(rqst_management_status_id)))

    rqst_management_step = clean_int_value_from_dict_object(rqst_case_management_dict,
                                                            "create_case_management_rows[{!s}]".format(rqst_case_row_index),
                                                            "management_step",
                                                            rqst_errors
                                                            )
    if rqst_management_step:
        if rqst_management_step > 9:
            rqst_errors.append(
                "management_step for create_case_management_rows[{!s}] must be < 9".format(
                    rqst_case_row_index))
    validated_c_m_row_params['rqst_management_step'] = rqst_management_step

    rqst_management_notes = clean_string_value_from_dict_object(rqst_case_management_dict,
                                                                "create_case_management_rows[{!s}]".format(
                                                                    rqst_case_row_index),
                                                                "management_notes",
                                                                rqst_errors,
                                                                empty_string_allowed=True
                                                                )
    validated_c_m_row_params['rqst_management_notes'] = rqst_management_notes

    return validated_c_m_row_params


def validate_delete_c_m_status_data(rqst_management_status_id, rqst_errors):
    validated_c_m_row_params = {
        'rqst_management_status_id': rqst_management_status_id
    }

    if rqst_management_status_id:
        try:
            case_status_row = CaseManagementStatus.objects.get(id=rqst_management_status_id)
        except CaseManagementStatus.DoesNotExist:
            rqst_errors.append('Case Management Status Row does not exist for the id: {!s}'.format(
                str(rqst_management_status_id)))
        except CaseManagementStatus.MultipleObjectsReturned:
            rqst_errors.append(
                'Multiple Case Management Status Rows exist for the id: {!s}'.format(
                    str(rqst_management_status_id)))
        except IntegrityError:
            rqst_errors.append(
                'Case Management Status Row already exists for the id: {!s}'.format(
                    str(rqst_management_status_id)))

    return validated_c_m_row_params


def validate_cps_info_params_for_add_instance_rqst(rqst_cps_info_params, rqst_consumer_met_nav_at, consumer_household_size, nav_instance, rqst_errors):
    rqst_primary_dependent_params = clean_dict_value_from_dict_object(rqst_cps_info_params,
                                                                    "cps_info",
                                                                    "primary_dependent",
                                                                      rqst_errors)
    primary_dependent_object = None
    if not rqst_errors:
        rqst_primary_dependent_database_id = clean_int_value_from_dict_object(rqst_primary_dependent_params,
                                                                              "primary_dependent",
                                                                              "Consumer Database ID",
                                                                              rqst_errors,
                                                                              no_key_allowed=True)
        if not rqst_primary_dependent_database_id:
            found_primary_dependent_PICConsumer_entries = check_consumer_db_entries_for_dependent_info(
                rqst_primary_dependent_params, rqst_errors)
            rqst_force_create_consumer = clean_bool_value_from_dict_object(rqst_primary_dependent_params, "root",
                                                                           "force_create_consumer", rqst_errors,
                                                                           no_key_allowed=True)

            if found_primary_dependent_PICConsumer_entries and not rqst_force_create_consumer:
                rqst_errors.append(
                    "The following PICConsumer object id(s) were found for given primary_dependent: {}. If you want to create a new consumer anyway, set cps_info['primary_dependent']['force_create_consumer'] to True.".format(
                        json.dumps(found_primary_dependent_PICConsumer_entries)))
            else:
                try:
                    primary_dependent_object = PICConsumer(first_name=rqst_primary_dependent_params["first_name"],
                                                           last_name=rqst_primary_dependent_params["last_name"],
                                                           met_nav_at=rqst_consumer_met_nav_at,
                                                           household_size=consumer_household_size,
                                                           navigator=nav_instance
                                                           )
                except IntegrityError:
                    rqst_errors.append("Error creating primary_dependent database entry for params: {!s}".format(
                        json.dumps(rqst_primary_dependent_params)))
        else:
            try:
                primary_dependent_object = PICConsumer.objects.get(id=rqst_primary_dependent_database_id)
            except PICConsumer.DoesNotExist:
                rqst_errors.append("PICConsumer object does not exist for primary_dependent Database ID: {!s}".format(
                    str(rqst_primary_dependent_database_id)))

    rqst_cps_location = clean_string_value_from_dict_object(rqst_cps_info_params, "cps_info", "cps_location", rqst_errors)

    apt_date_dict = clean_dict_value_from_dict_object(rqst_cps_info_params,
                                                      "cps_info",
                                                      "apt_date",
                                                      rqst_errors)
    rqst_apt_date = None
    if apt_date_dict is not None:
        month = clean_int_value_from_dict_object(apt_date_dict, "date_met_nav", "Month", rqst_errors)
        if month:
            if month < 1 or month > 12:
                rqst_errors.append("Month must be between 1 and 12 inclusive")

        day = clean_int_value_from_dict_object(apt_date_dict, "date_met_nav", "Day", rqst_errors)
        if day:
            if day < 1 or day > 31:
                rqst_errors.append("Day must be between 1 and 31 inclusive")

        year = clean_int_value_from_dict_object(apt_date_dict, "date_met_nav", "Year", rqst_errors)
        if year:
            if year < 1 or year > 9999:
                rqst_errors.append("Year must be between 1 and 9999 inclusive")

        if not rqst_errors:
            rqst_apt_date = datetime.date(year, month, day)

    rqst_target_list = clean_bool_value_from_dict_object(rqst_cps_info_params,
                                                         "cps_info",
                                                         "target_list",
                                                         rqst_errors)
    rqst_phone_apt = clean_bool_value_from_dict_object(rqst_cps_info_params,
                                                       "cps_info",
                                                       "phone_apt",
                                                       rqst_errors)
    rqst_case_mgmt_type = clean_string_value_from_dict_object(rqst_cps_info_params,
                                                              "cps_info",
                                                              "case_mgmt_type",
                                                              rqst_errors)
    rqst_case_mgmt_status = clean_string_value_from_dict_object(rqst_cps_info_params,
                                                                "cps_info",
                                                                "case_mgmt_status",
                                                                rqst_errors)

    rqst_secondary_dependents = clean_list_value_from_dict_object(rqst_cps_info_params,
                                                                  "cps_info",
                                                                  "secondary_dependents",
                                                                  rqst_errors,
                                                                  no_key_allowed=True,
                                                                  empty_list_allowed=True)
    secondary_dependents_list = []
    if rqst_secondary_dependents:
        for dependent_index, rqst_secondary_dependent_dict in enumerate(rqst_secondary_dependents):
            secondary_dependent_object = None
            if not rqst_errors:
                rqst_secondary_dependent_database_id = clean_int_value_from_dict_object(rqst_secondary_dependent_dict,
                                                                                        "secondary_dependent",
                                                                                        "Consumer Database ID",
                                                                                        rqst_errors,
                                                                                        no_key_allowed=True)

                if not rqst_secondary_dependent_database_id:
                    found_secondary_dependent_PICConsumer_entries = check_consumer_db_entries_for_dependent_info(
                        rqst_secondary_dependent_dict, rqst_errors)
                    rqst_force_create_consumer = clean_bool_value_from_dict_object(rqst_secondary_dependent_dict,
                                                                                   "root",
                                                                                   "force_create_consumer", rqst_errors,
                                                                                   no_key_allowed=True)

                    if found_secondary_dependent_PICConsumer_entries and not rqst_force_create_consumer:
                        rqst_errors.append(
                            "The following PICConsumer object id(s) were found for the secondary_dependent at index {}: {}. If you want to create a new consumer anyway, set cps_info['secondary_dependents'][index]['force_create_consumer'] to True.".format(
                                dependent_index,
                                json.dumps(found_secondary_dependent_PICConsumer_entries)))
                    else:
                        try:
                            secondary_dependent_object = PICConsumer(
                                first_name=rqst_secondary_dependent_dict["first_name"],
                                last_name=rqst_secondary_dependent_dict["last_name"],
                                met_nav_at=rqst_consumer_met_nav_at,
                                household_size=consumer_household_size,
                                navigator=nav_instance)
                        except IntegrityError:
                            rqst_errors.append(
                                "Error creating secondary_dependent database entry for params: {!s}".format(
                                    json.dumps(rqst_secondary_dependent_dict)))
                else:
                    try:
                        secondary_dependent_object = PICConsumer.objects.get(id=rqst_secondary_dependent_database_id)
                    except PICConsumer.DoesNotExist:
                        rqst_errors.append(
                            "PICConsumer object does not exist for secondary_dependent with index({!s}) and Database ID: {!s}".format(
                                str(dependent_index),
                                str(rqst_secondary_dependent_database_id)))

            secondary_dependents_list.append(secondary_dependent_object)

    rqst_app_type = clean_string_value_from_dict_object(rqst_cps_info_params,
                                                        "cps_info",
                                                        "app_type",
                                                        rqst_errors)
    rqst_app_status = clean_string_value_from_dict_object(rqst_cps_info_params,
                                                          "cps_info",
                                                          "app_status",
                                                          rqst_errors)
    rqst_point_of_origin = clean_string_value_from_dict_object(rqst_cps_info_params,
                                                          "cps_info",
                                                          "point_of_origin",
                                                          rqst_errors)

    cps_info_params = {
        "rqst_cps_location": rqst_cps_location,
        "rqst_apt_date": rqst_apt_date,
        "rqst_target_list": rqst_target_list,
        "rqst_phone_apt": rqst_phone_apt,
        "rqst_case_mgmt_type": rqst_case_mgmt_type,
        "rqst_case_mgmt_status": rqst_case_mgmt_status,
        "rqst_app_type": rqst_app_type,
        "rqst_app_status": rqst_app_status,
        "rqst_point_of_origin": rqst_point_of_origin,
        "primary_dependent_object": primary_dependent_object,
        "secondary_dependents_list": secondary_dependents_list
    }

    return cps_info_params


def check_consumer_db_entries_for_dependent_info(rqst_dependent_dict, rqst_errors):
    """
    This function takes a dictionary populated with dependent information and checks to see if there are any PICConsumer
    database entries that exist for it.

    :param rqst_dependent_dict: (type: dictionary) dependent information
    :param rqst_errors: (type: list) list of error messages
    :return: (type: list) list of id's for found PICConsumer entries
    """

    found_consumer_entries = []

    rqst_dependent_f_name = clean_string_value_from_dict_object(rqst_dependent_dict,
                                                                "dependent_info",
                                                                "first_name",
                                                                rqst_errors)
    rqst_dependent_l_name = clean_string_value_from_dict_object(rqst_dependent_dict,
                                                                "dependent_info",
                                                                "last_name",
                                                                rqst_errors)

    if not rqst_errors:
        consumer_entry_query = PICConsumer.objects.filter(first_name__iexact=rqst_dependent_f_name,
                                                          last_name__iexact=rqst_dependent_l_name)
        for consumer_entry in consumer_entry_query:
            found_consumer_entries.append(consumer_entry.id)

    return found_consumer_entries


def validate_cps_info_params_for_modify_instance_rqst(rqst_cps_info_params, consumer_instance, rqst_consumer_met_nav_at, rqst_consumer_household_size, rqst_nav_instance, rqst_errors):
    validated_params = {}

    if not rqst_consumer_met_nav_at:
        rqst_consumer_met_nav_at = consumer_instance.met_nav_at
    if not rqst_consumer_household_size:
        rqst_consumer_household_size = consumer_instance.household_size
    if not rqst_nav_instance:
        rqst_nav_instance = consumer_instance.navigator

    if "primary_dependent" in rqst_cps_info_params:
        rqst_primary_dependent_dict = clean_dict_value_from_dict_object(rqst_cps_info_params,
                                                                        "cps_info",
                                                                        "primary_dependent",
                                                                        rqst_errors)
        primary_dependent_object = None
        if not rqst_errors:
            rqst_primary_dependent_database_id = clean_int_value_from_dict_object(rqst_primary_dependent_dict,
                                                                                  "primary_dependent",
                                                                                  "Consumer Database ID",
                                                                                  rqst_errors,
                                                                                  no_key_allowed=True)
            if not rqst_primary_dependent_database_id:
                found_primary_dependent_PICConsumer_entries = check_consumer_db_entries_for_dependent_info(
                    rqst_primary_dependent_dict, rqst_errors)
                rqst_force_create_consumer = clean_bool_value_from_dict_object(rqst_primary_dependent_dict, "root",
                                                                               "force_create_consumer", rqst_errors,
                                                                               no_key_allowed=True)

                if found_primary_dependent_PICConsumer_entries and not rqst_force_create_consumer:
                    rqst_errors.append(
                        "The following PICConsumer object id(s) were found for given primary_dependent: {}. If you want to create a new consumer anyway, set cps_info['primary_dependent']['force_create_consumer'] to True.".format(
                            json.dumps(found_primary_dependent_PICConsumer_entries)))
                else:
                    try:
                        primary_dependent_object = PICConsumer(first_name=rqst_primary_dependent_dict["first_name"],
                                                               last_name=rqst_primary_dependent_dict["last_name"],
                                                               met_nav_at=rqst_consumer_met_nav_at,
                                                               household_size=rqst_consumer_household_size,
                                                               navigator=rqst_nav_instance
                                                               )
                    except IntegrityError:
                        rqst_errors.append("Error creating primary_dependent database entry for params: {!s}".format(
                            json.dumps(rqst_primary_dependent_dict)))
            else:
                try:
                    primary_dependent_object = PICConsumer.objects.get(id=rqst_primary_dependent_database_id)
                except PICConsumer.DoesNotExist:
                    rqst_errors.append("PICConsumer object does not exist for primary_dependent Database ID: {!s}".format(
                        str(rqst_primary_dependent_database_id)))

        validated_params["primary_dependent_object"] = primary_dependent_object
    if "secondary_dependents" in rqst_cps_info_params:
        rqst_secondary_dependents = clean_list_value_from_dict_object(rqst_cps_info_params,
                                                                      "cps_info",
                                                                      "secondary_dependents",
                                                                      rqst_errors,
                                                                      no_key_allowed=True,
                                                                      empty_list_allowed=True)
        validated_params["secondary_dependents_list"] = rqst_secondary_dependents

        secondary_dependents_list = []
        if rqst_secondary_dependents:
            for dependent_index, rqst_secondary_dependent_dict in enumerate(rqst_secondary_dependents):
                secondary_dependent_object = None
                if not rqst_errors:
                    rqst_secondary_dependent_database_id = clean_int_value_from_dict_object(
                        rqst_secondary_dependent_dict,
                        "secondary_dependent",
                        "Consumer Database ID",
                        rqst_errors,
                        no_key_allowed=True)
                    if not rqst_secondary_dependent_database_id:
                        found_secondary_dependent_PICConsumer_entries = check_consumer_db_entries_for_dependent_info(
                            rqst_secondary_dependent_dict, rqst_errors)
                        rqst_force_create_consumer = clean_bool_value_from_dict_object(rqst_secondary_dependent_dict,
                                                                                       "root",
                                                                                       "force_create_consumer",
                                                                                       rqst_errors,
                                                                                       no_key_allowed=True)

                        if found_secondary_dependent_PICConsumer_entries and not rqst_force_create_consumer:
                            rqst_errors.append(
                                "The following PICConsumer object id(s) were found for the secondary_dependent at index {}: {}. If you want to create a new consumer anyway, set cps_info['secondary_dependents'][index]['force_create_consumer'] to True.".format(
                                    dependent_index,
                                    json.dumps(found_secondary_dependent_PICConsumer_entries)))
                        else:
                            try:
                                secondary_dependent_object = PICConsumer(
                                    first_name=rqst_secondary_dependent_dict["first_name"],
                                    last_name=rqst_secondary_dependent_dict["last_name"],
                                    met_nav_at=rqst_consumer_met_nav_at,
                                    household_size=rqst_consumer_household_size,
                                    navigator=rqst_nav_instance)
                            except IntegrityError:
                                rqst_errors.append(
                                    "Error creating secondary_dependent database entry for params: {!s}".format(
                                        json.dumps(rqst_secondary_dependent_dict)))
                    else:
                        try:
                            secondary_dependent_object = PICConsumer.objects.get(
                                id=rqst_secondary_dependent_database_id)
                        except PICConsumer.DoesNotExist:
                            rqst_errors.append(
                                "PICConsumer object does not exist for secondary_dependent with index({!s}) and Database ID: {!s}".format(
                                    str(dependent_index),
                                    str(rqst_secondary_dependent_database_id)))

                secondary_dependents_list.append(secondary_dependent_object)

            validated_params["secondary_dependents_list"] = secondary_dependents_list
    if "cps_location" in rqst_cps_info_params:
        rqst_cps_location = clean_string_value_from_dict_object(rqst_cps_info_params, "cps_info", "cps_location", rqst_errors)

        validated_params["rqst_cps_location"] = rqst_cps_location
    if "apt_date" in rqst_cps_info_params:
        apt_date_dict = clean_dict_value_from_dict_object(rqst_cps_info_params,
                                                          "cps_info",
                                                          "apt_date",
                                                          rqst_errors)
        rqst_apt_date = None
        if apt_date_dict is not None:
            month = clean_int_value_from_dict_object(apt_date_dict, "date_met_nav", "Month", rqst_errors)
            if month:
                if month < 1 or month > 12:
                    rqst_errors.append("Month must be between 1 and 12 inclusive")

            day = clean_int_value_from_dict_object(apt_date_dict, "date_met_nav", "Day", rqst_errors)
            if day:
                if day < 1 or day > 31:
                    rqst_errors.append("Day must be between 1 and 31 inclusive")

            year = clean_int_value_from_dict_object(apt_date_dict, "date_met_nav", "Year", rqst_errors)
            if year:
                if year < 1 or year > 9999:
                    rqst_errors.append("Year must be between 1 and 9999 inclusive")

            if not rqst_errors:
                rqst_apt_date = datetime.date(year, month, day)

        validated_params["rqst_apt_date"] = rqst_apt_date
    if "target_list" in rqst_cps_info_params:
        rqst_target_list = clean_bool_value_from_dict_object(rqst_cps_info_params,
                                                             "cps_info",
                                                             "target_list",
                                                             rqst_errors)

        validated_params["rqst_target_list"] = rqst_target_list
    if "phone_apt" in rqst_cps_info_params:
        rqst_phone_apt = clean_bool_value_from_dict_object(rqst_cps_info_params,
                                                           "cps_info",
                                                           "phone_apt",
                                                           rqst_errors)

        validated_params["rqst_phone_apt"] = rqst_phone_apt
    if "case_mgmt_type" in rqst_cps_info_params:
        rqst_case_mgmt_type = clean_string_value_from_dict_object(rqst_cps_info_params,
                                                                  "cps_info",
                                                                  "case_mgmt_type",
                                                                  rqst_errors)

        validated_params["rqst_case_mgmt_type"] = rqst_case_mgmt_type
    if "case_mgmt_status" in rqst_cps_info_params:
        rqst_case_mgmt_status = clean_string_value_from_dict_object(rqst_cps_info_params,
                                                                    "cps_info",
                                                                    "case_mgmt_status",
                                                                    rqst_errors)

        validated_params["rqst_case_mgmt_status"] = rqst_case_mgmt_status
    if "app_type" in rqst_cps_info_params:
        rqst_app_type = clean_string_value_from_dict_object(rqst_cps_info_params,
                                                            "cps_info",
                                                            "app_type",
                                                            rqst_errors)

        validated_params["rqst_app_type"] = rqst_app_type
    if "app_status" in rqst_cps_info_params:
        rqst_app_status = clean_string_value_from_dict_object(rqst_cps_info_params,
                                                              "cps_info",
                                                              "app_status",
                                                              rqst_errors)

        validated_params["rqst_app_status"] = rqst_app_status
    if "point_of_origin" in rqst_cps_info_params:
        rqst_point_of_origin = clean_string_value_from_dict_object(rqst_cps_info_params,
                                                              "cps_info",
                                                              "point_of_origin",
                                                              rqst_errors)

        validated_params["rqst_point_of_origin"] = rqst_point_of_origin

    return validated_params


def validate_indiv_seeking_nav_params(rqst_body, validated_params, rqst_errors):
    if 'billing_amount' in rqst_body:
        validated_params['billing_amount'] = clean_float_value_from_dict_object(
            rqst_body,
            "root",
            'billing_amount',
            rqst_errors,
            none_allowed=True,
        )
        if validated_params['billing_amount'] and validated_params['billing_amount'] < 0:
            rqst_errors.append(
                "Value for 'billing_amount' must be greater than 0. Given value is: {}".format(
                    validated_params['billing_amount']
                )
            )
    if 'consumer_need' in rqst_body:
        validated_params['consumer_need'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            'consumer_need',
            rqst_errors,
            empty_string_allowed=True
        )
        if validated_params['consumer_need'] == '':
            validated_params['consumer_need'] = 'not available'
    if 'service_expertise_need' in rqst_body:
        validated_params['service_expertise_need'] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            'service_expertise_need',
            rqst_errors,
            empty_string_allowed=True
        )
    if 'insurance_carrier' in rqst_body:
        carrier_dict = clean_dict_value_from_dict_object(
            rqst_body,
            "root",
            'insurance_carrier',
            rqst_errors,
            none_allowed=True
        )
        validated_carrier_info = None
        if carrier_dict:
            validated_carrier_info = {
                "name": clean_string_value_from_dict_object(
                    carrier_dict,
                    "insurance_carrier",
                    'name',
                    rqst_errors,
                    empty_string_allowed=True
                ),
                "state_province": clean_string_value_from_dict_object(
                    carrier_dict,
                    "insurance_carrier",
                    'state_province',
                    rqst_errors,
                    empty_string_allowed=True
                )
            }
        validated_params['insurance_carrier'] = validated_carrier_info

    if 'add_healthcare_locations_used' in rqst_body:
        add_healthcare_locations_used = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "add_healthcare_locations_used",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_location_info = []
        for location_dict in add_healthcare_locations_used:
            if not isinstance(location_dict, dict):
                rqst_errors.append('Error: A location object in \'add_healthcare_locations_used\' is not a object.')
            else:
                location_info = {
                    "name": clean_string_value_from_dict_object(
                        location_dict,
                        "add_location_object",
                        'name',
                        rqst_errors
                    ),
                    "state_province": clean_string_value_from_dict_object(
                        location_dict,
                        "add_location_object",
                        'state_province',
                        rqst_errors,
                        none_allowed=True
                    )
                }
                if not location_info['state_province']:
                    location_info['state_province'] = 'not available'

                validated_location_info.append(location_info)

        validated_params['add_healthcare_locations_used'] = validated_location_info
    elif 'remove_healthcare_locations_used' in rqst_body:
        remove_healthcare_locations_used = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "remove_healthcare_locations_used",
            rqst_errors
        )

        validated_location_info = []
        for location_dict in remove_healthcare_locations_used:
            if not isinstance(location_dict, dict):
                rqst_errors.append('Error: A location object in \'remove_healthcare_locations_used\' is not a object.')
            else:
                location_info = {
                    "name": clean_string_value_from_dict_object(
                        location_dict,
                        "remove_location_object",
                        'name',
                        rqst_errors
                    ),
                    "state_province": clean_string_value_from_dict_object(
                        location_dict,
                        "remove_location_object",
                        'state_province',
                        rqst_errors,
                        none_allowed=True
                    )
                }
                if not location_info['state_province']:
                    location_info['state_province'] = 'not available'

                validated_location_info.append(location_info)

        validated_params['remove_healthcare_locations_used'] = validated_location_info
