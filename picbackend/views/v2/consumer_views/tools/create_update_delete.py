"""
Defines utility functions and classes for consumer views
"""

import datetime
import json
from ...utils import clean_string_value_from_dict_object
from ...utils import clean_int_value_from_dict_object
from ...utils import clean_list_value_from_dict_object
from ...utils import clean_dict_value_from_dict_object
from ...utils import clean_bool_value_from_dict_object
from picmodels.models import PICStaff
from picmodels.models import PICConsumer
from picmodels.models import NavMetricsLocation
from picmodels.services.staff_consumer_models_services.pic_consumer_services import add_instance_using_validated_params
from picmodels.services.staff_consumer_models_services.pic_consumer_services import modify_instance_using_validated_params
from picmodels.services.staff_consumer_models_services.pic_consumer_services import delete_instance_using_validated_params
from django.db import IntegrityError
from django.core.validators import validate_email
from django import forms


def validate_rqst_params_and_add_instance(response_raw_data, rqst_consumer_info, post_errors):
    """
    This function takes dictionary populated with PIC consumer info, parses for errors, adds the consumer
    to the database if there are none, and adds the consumer info to given response data.

    :param response_raw_data: (type: dictionary) dictionary that contains response data
    :param rqst_consumer_info: (type: dictionary) dictionary that contains consumer info
    :param post_errors: (type: list) list of error messages
    :return: (type: dictionary) dictionary that contains response data
    """

    add_consumer_params = get_consumer_mgmt_put_params(rqst_consumer_info, post_errors)
    if not add_consumer_params['rqst_cps_consumer']:
        add_consumer_params['rqst_cps_consumer'] = False
    add_consumer_params['force_create_consumer'] = clean_bool_value_from_dict_object(rqst_consumer_info,
                                                                                     "root",
                                                                                     "force_create_consumer",
                                                                                     post_errors,
                                                                                     no_key_allowed=True)

    if not post_errors:
        matching_consumer_instances, consumer_instance, backup_consumer_obj = add_instance_using_validated_params(add_consumer_params, post_errors)

        if matching_consumer_instances:
            consumer_match_data = []
            for consumer in matching_consumer_instances:
                consumer_match_data.append(consumer.return_values_dict())
            response_raw_data['Data']['Possible Consumer Matches'] = consumer_match_data
        else:
            if consumer_instance:
                response_raw_data['Data']["Database ID"] = consumer_instance.id
            if backup_consumer_obj:
                response_raw_data['Data']["backup_consumer"] = backup_consumer_obj.return_values_dict()


def get_consumer_mgmt_put_params(post_data, post_errors):
    """
    This function parses the BODY of requests for PIC consumer management PUT requests, checks for errors, and returns
    relevant information as a dictionary

    :param post_data: (type: dictionary) PUT information to be parsed
    :param post_errors: (type: list) list of error messages
    :return: (type: dictionary) dictionary with relevant consumer information
    """

    rqst_consumer_email = clean_string_value_from_dict_object(post_data, "root", "Email", post_errors,
                                                              empty_string_allowed=True)
    if rqst_consumer_email and not post_errors:
        try:
            validate_email(rqst_consumer_email)
        except forms.ValidationError:
            post_errors.append("{!s} must be a valid email address".format(rqst_consumer_email))
    rqst_consumer_f_name = clean_string_value_from_dict_object(post_data, "root", "First Name", post_errors)
    rqst_consumer_m_name = clean_string_value_from_dict_object(post_data, "root", "Middle Name", post_errors,
                                                               empty_string_allowed=True)
    rqst_consumer_l_name = clean_string_value_from_dict_object(post_data, "root", "Last Name", post_errors)
    rqst_consumer_plan = clean_string_value_from_dict_object(post_data, "root", "Plan", post_errors,
                                                             empty_string_allowed=True)
    rqst_consumer_met_nav_at = clean_string_value_from_dict_object(post_data, "root", "Met Navigator At", post_errors)
    rqst_consumer_household_size = clean_int_value_from_dict_object(post_data, "root", "Household Size", post_errors)
    rqst_consumer_phone = clean_string_value_from_dict_object(post_data, "root", "Phone Number", post_errors,
                                                              empty_string_allowed=True)
    rqst_consumer_pref_lang = clean_string_value_from_dict_object(post_data, "root", "Preferred Language", post_errors,
                                                                  empty_string_allowed=True)
    rqst_navigator_notes = clean_list_value_from_dict_object(post_data, "root", "Navigator Notes", post_errors,
                                                             empty_list_allowed=True)

    rqst_address_line_1 = clean_string_value_from_dict_object(post_data, "root", "Address Line 1", post_errors,
                                                              empty_string_allowed=True)
    rqst_address_line_2 = clean_string_value_from_dict_object(post_data, "root", "Address Line 2", post_errors,
                                                              empty_string_allowed=True)
    if rqst_address_line_2 is None:
        rqst_address_line_2 = ''
    rqst_city = clean_string_value_from_dict_object(post_data, "root", "City", post_errors, empty_string_allowed=True)
    rqst_state = clean_string_value_from_dict_object(post_data, "root", "State", post_errors, empty_string_allowed=True)
    rqst_zipcode = clean_string_value_from_dict_object(post_data, "root", "Zipcode", post_errors,
                                                       empty_string_allowed=True)

    date_met_nav_dict = clean_dict_value_from_dict_object(post_data, "root", "date_met_nav", post_errors,
                                                          none_allowed=True)
    rqst_date_met_nav = None
    if date_met_nav_dict is not None:
        month = clean_int_value_from_dict_object(date_met_nav_dict, "date_met_nav", "Month", post_errors)
        if month < 1 or month > 12:
            post_errors.append("Month must be between 1 and 12 inclusive")

        day = clean_int_value_from_dict_object(date_met_nav_dict, "date_met_nav", "Day", post_errors)
        if day < 1 or day > 31:
            post_errors.append("Day must be between 1 and 31 inclusive")

        year = clean_int_value_from_dict_object(date_met_nav_dict, "date_met_nav", "Year", post_errors)
        if year < 1 or year > 9999:
            post_errors.append("Year must be between 1 and 9999 inclusive")

        if len(post_errors) == 0:
            rqst_date_met_nav = datetime.date(year, month, day)

    rqst_nav_id = clean_int_value_from_dict_object(post_data, "root", "Navigator Database ID", post_errors)
    nav_instance = None
    if rqst_nav_id and not post_errors:
        try:
            nav_instance = PICStaff.objects.get(id=rqst_nav_id)
        except PICStaff.DoesNotExist:
            post_errors.append('Staff database entry does not exist for the navigator id: {}'.format(rqst_nav_id))

    rqst_cps_consumer = clean_bool_value_from_dict_object(post_data,
                                                          "root",
                                                          "cps_consumer",
                                                          post_errors,
                                                          no_key_allowed=True)
    rqst_cps_info_dict = None
    validated_cps_info_dict = None
    if rqst_cps_consumer:
        rqst_cps_info_dict = clean_dict_value_from_dict_object(post_data,
                                                               "root",
                                                               "cps_info",
                                                               post_errors,
                                                               no_key_allowed=True)
        validated_cps_info_dict = get_consumer_cps_info_put_params(rqst_cps_info_dict, rqst_date_met_nav, rqst_consumer_household_size, nav_instance, post_errors)

    rqst_create_backup = clean_bool_value_from_dict_object(post_data,
                                                           "root",
                                                           "create_backup",
                                                           post_errors,
                                                           no_key_allowed=True)

    return {"rqst_consumer_email": rqst_consumer_email,
            "rqst_consumer_f_name": rqst_consumer_f_name,
            "rqst_consumer_m_name": rqst_consumer_m_name,
            "rqst_consumer_l_name": rqst_consumer_l_name,
            "rqst_consumer_plan": rqst_consumer_plan,
            "rqst_consumer_met_nav_at": rqst_consumer_met_nav_at,
            "rqst_consumer_household_size": rqst_consumer_household_size,
            "rqst_consumer_phone": rqst_consumer_phone,
            "rqst_consumer_pref_lang": rqst_consumer_pref_lang,
            "rqst_navigator_notes": rqst_navigator_notes,
            "rqst_nav_id": rqst_nav_id,
            "nav_instance": nav_instance,
            "rqst_address_line_1": rqst_address_line_1,
            "rqst_address_line_2": rqst_address_line_2,
            "rqst_city": rqst_city,
            "rqst_state": rqst_state,
            "rqst_zipcode": rqst_zipcode,
            "rqst_date_met_nav": rqst_date_met_nav,
            "rqst_cps_consumer": rqst_cps_consumer,
            "rqst_cps_info_dict": rqst_cps_info_dict,
            "validated_cps_info_dict": validated_cps_info_dict,
            "rqst_create_backup": rqst_create_backup}


def get_consumer_cps_info_put_params(rqst_cps_info_dict, date_met_nav, consumer_household_size, nav_instance, post_errors):
    rqst_primary_dependent_dict = clean_dict_value_from_dict_object(rqst_cps_info_dict,
                                                                    "cps_info",
                                                                    "primary_dependent",
                                                                    post_errors)
    primary_dependent_object = None
    if len(post_errors) == 0:
        rqst_primary_dependent_database_id = clean_int_value_from_dict_object(rqst_primary_dependent_dict,
                                                                              "primary_dependent",
                                                                              "Consumer Database ID",
                                                                              post_errors,
                                                                              no_key_allowed=True)
        if not rqst_primary_dependent_database_id:
            primary_dependent_found_PICConsumer_entries = check_consumer_db_entries_for_dependent_info(
                rqst_primary_dependent_dict, post_errors)
            if not primary_dependent_found_PICConsumer_entries:
                try:
                    primary_dependent_object = PICConsumer(first_name=rqst_primary_dependent_dict["first_name"],
                                                           last_name=rqst_primary_dependent_dict["last_name"],
                                                           met_nav_at=date_met_nav,
                                                           household_size=consumer_household_size,
                                                           navigator=nav_instance
                                                           )
                except IntegrityError:
                    post_errors.append("Error creating primary_dependent database entry for params: {!s}".format(
                        json.dumps(rqst_primary_dependent_dict)))
            else:
                post_errors.append(
                    "The following PICConsumer object id(s) were found for given primary_dependent: {}".format(
                        json.dumps(primary_dependent_found_PICConsumer_entries)))
        else:
            try:
                primary_dependent_object = PICConsumer.objects.get(id=rqst_primary_dependent_database_id)
            except PICConsumer.DoesNotExist:
                post_errors.append("PICConsumer object does not exist for primary_dependent Database ID: {!s}".format(
                    str(rqst_primary_dependent_database_id)))

    rqst_cps_location = clean_string_value_from_dict_object(rqst_cps_info_dict, "cps_info", "cps_location", post_errors)

    apt_date_dict = clean_dict_value_from_dict_object(rqst_cps_info_dict,
                                                      "cps_info",
                                                      "apt_date",
                                                      post_errors)
    rqst_apt_date = None
    if apt_date_dict is not None:
        month = clean_int_value_from_dict_object(apt_date_dict, "date_met_nav", "Month", post_errors)
        if month < 1 or month > 12:
            post_errors.append("Month must be between 1 and 12 inclusive")

        day = clean_int_value_from_dict_object(apt_date_dict, "date_met_nav", "Day", post_errors)
        if day < 1 or day > 31:
            post_errors.append("Day must be between 1 and 31 inclusive")

        year = clean_int_value_from_dict_object(apt_date_dict, "date_met_nav", "Year", post_errors)
        if year < 1 or year > 9999:
            post_errors.append("Year must be between 1 and 9999 inclusive")

        if len(post_errors) == 0:
            rqst_apt_date = datetime.date(year, month, day)

    rqst_target_list = clean_bool_value_from_dict_object(rqst_cps_info_dict,
                                                         "cps_info",
                                                         "target_list",
                                                         post_errors)
    rqst_phone_apt = clean_bool_value_from_dict_object(rqst_cps_info_dict,
                                                       "cps_info",
                                                       "phone_apt",
                                                       post_errors)
    rqst_case_mgmt_type = clean_string_value_from_dict_object(rqst_cps_info_dict,
                                                              "cps_info",
                                                              "case_mgmt_type",
                                                              post_errors)
    rqst_case_mgmt_status = clean_string_value_from_dict_object(rqst_cps_info_dict,
                                                                "cps_info",
                                                                "case_mgmt_status",
                                                                post_errors)

    rqst_secondary_dependents = clean_list_value_from_dict_object(rqst_cps_info_dict,
                                                                  "cps_info",
                                                                  "secondary_dependents",
                                                                  post_errors,
                                                                  no_key_allowed=True)
    secondary_dependents_list = []
    if rqst_secondary_dependents:
        for dependent_index, rqst_secondary_dependent_dict in enumerate(rqst_secondary_dependents):
            secondary_dependent_object = None
            if len(post_errors) == 0:
                rqst_secondary_dependent_database_id = clean_int_value_from_dict_object(rqst_secondary_dependent_dict,
                                                                                        "secondary_dependent",
                                                                                        "Consumer Database ID",
                                                                                        post_errors,
                                                                                        no_key_allowed=True)
                if not rqst_secondary_dependent_database_id:
                    secondary_dependent_found_PICConsumer_entries = check_consumer_db_entries_for_dependent_info(
                        rqst_secondary_dependent_dict, post_errors)
                    if not secondary_dependent_found_PICConsumer_entries:
                        try:
                            secondary_dependent_object = PICConsumer(
                                first_name=rqst_secondary_dependent_dict["first_name"],
                                last_name=rqst_secondary_dependent_dict["last_name"],
                                met_nav_at=date_met_nav,
                                household_size=consumer_household_size,
                                navigator=nav_instance)
                        except IntegrityError:
                            post_errors.append(
                                "Error creating secondary_dependent database entry for params: {!s}".format(
                                    json.dumps(rqst_secondary_dependent_dict)))
                    else:
                        post_errors.append(
                            "The following PICConsumer object id(s) were found for the secondary_dependent at index {}: {}".format(
                                dependent_index,
                                json.dumps(secondary_dependent_found_PICConsumer_entries)))
                else:
                    try:
                        secondary_dependent_object = PICConsumer.objects.get(id=rqst_secondary_dependent_database_id)
                    except NavMetricsLocation.DoesNotExist:
                        post_errors.append(
                            "PICConsumer object does not exist for secondary_dependent with index({!s}) and Database ID: {!s}".format(
                                str(dependent_index),
                                str(rqst_secondary_dependent_database_id)))

            secondary_dependents_list.append(secondary_dependent_object)

    rqst_app_type = clean_string_value_from_dict_object(rqst_cps_info_dict,
                                                        "cps_info",
                                                        "app_type",
                                                        post_errors)
    rqst_app_status = clean_string_value_from_dict_object(rqst_cps_info_dict,
                                                          "cps_info",
                                                          "app_status",
                                                          post_errors)

    cps_info_params = {
        "rqst_cps_location": rqst_cps_location,
        "rqst_apt_date": rqst_apt_date,
        "rqst_target_list": rqst_target_list,
        "rqst_phone_apt": rqst_phone_apt,
        "rqst_case_mgmt_type": rqst_case_mgmt_type,
        "rqst_case_mgmt_status": rqst_case_mgmt_status,
        "rqst_app_type": rqst_app_type,
        "rqst_app_status": rqst_app_status,
        "primary_dependent_object": primary_dependent_object,
        "secondary_dependents_list": secondary_dependents_list
    }

    return cps_info_params


def check_consumer_db_entries_for_dependent_info(rqst_dependent_dict, post_errors):
    """
    This function takes a dictionary populated with dependent information and checks to see if there are any PICConsumer
    database entries that exist for it.

    :param rqst_dependent_dict: (type: dictionary) dependent information
    :param post_errors: (type: list) list of error messages
    :return: (type: list) list of id's for found PICConsumer entries
    """

    found_consumer_entries = []

    rqst_dependent_f_name = clean_string_value_from_dict_object(rqst_dependent_dict,
                                                                "dependent_info",
                                                                "first_name",
                                                                post_errors)
    rqst_dependent_l_name = clean_string_value_from_dict_object(rqst_dependent_dict,
                                                                "dependent_info",
                                                                "last_name",
                                                                post_errors)

    if len(post_errors) == 0:
        consumer_entry_query = PICConsumer.objects.filter(first_name=rqst_dependent_f_name,
                                                          last_name=rqst_dependent_l_name)
        for consumer_entry in consumer_entry_query:
            found_consumer_entries.append(consumer_entry.id)

    return found_consumer_entries


def validate_rqst_params_and_modify_instance(response_raw_data, post_data, post_errors):
    """
    This function takes dictionary populated with PIC consumer info, parses for errors, and modifies the consumer
    instance if there are none.

    :param response_raw_data: (type: dictionary) dictionary that contains response data
    :param post_data: (type: dictionary) dictionary with PIC consumer info
    :param post_errors: (type: list) list of error messages
    :return: (type: dictionary) dictionary that contains response data
    """

    modify_consumer_params = get_consumer_mgmt_put_params(post_data, post_errors)
    modify_consumer_params['rqst_consumer_id'] = clean_int_value_from_dict_object(post_data, "root", "Consumer Database ID", post_errors)

    if not post_errors:
        consumer_instance, backup_consumer_obj = modify_instance_using_validated_params(modify_consumer_params, post_errors)

        if not post_errors:
            if consumer_instance:
                response_raw_data['Data']["Database ID"] = consumer_instance.id
            if backup_consumer_obj:
                response_raw_data['Data']["backup_consumer"] = backup_consumer_obj.return_values_dict()


def validate_rqst_params_and_delete_instance(response_raw_data, post_data, post_errors):
    """
    This function takes dictionary populated with PIC consumer info, parses for errors, and deletes the consumer
    instance if there are none.

    :param response_raw_data: (type: dictionary) dictionary that contains response data
    :param post_data: (type: dictionary) dictionary with PIC consumer info
    :param post_errors: (type: list) list of error messages
    :return: (type: dictionary) dictionary that contains response data
    """

    rqst_consumer_id = clean_int_value_from_dict_object(post_data, "root", "Consumer Database ID", post_errors)
    rqst_create_backup = clean_bool_value_from_dict_object(post_data,
                                                          "root",
                                                          "create_backup",
                                                          post_errors,
                                                          no_key_allowed=True)

    if not post_errors:
        backup_consumer_obj = delete_instance_using_validated_params(rqst_consumer_id, rqst_create_backup, post_errors)

        if not post_errors:
            response_raw_data['Data']["Database ID"] = "Deleted"

            if backup_consumer_obj:
                response_raw_data['Data']["backup_consumer"] = backup_consumer_obj.return_values_dict()
