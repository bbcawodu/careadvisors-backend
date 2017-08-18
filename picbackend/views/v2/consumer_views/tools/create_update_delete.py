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
from picmodels.services.staff_consumer_models_services.pic_consumer_services import add_instance_using_validated_params
from picmodels.services.staff_consumer_models_services.pic_consumer_services import modify_instance_using_validated_params
from picmodels.services.staff_consumer_models_services.pic_consumer_services import delete_instance_using_validated_params
from django.db import IntegrityError
from django.core.validators import validate_email
from django import forms


def validate_rqst_params_and_add_instance(rqst_consumer_info, rqst_errors):
    add_consumer_params = validate_add_instance_rqst_params(rqst_consumer_info, rqst_errors)
    if not add_consumer_params['rqst_cps_consumer']:
        add_consumer_params['rqst_cps_consumer'] = False
    add_consumer_params['force_create_consumer'] = clean_bool_value_from_dict_object(rqst_consumer_info,
                                                                                     "root",
                                                                                     "force_create_consumer",
                                                                                     rqst_errors,
                                                                                     no_key_allowed=True)

    matching_consumer_instances = None
    consumer_instance = None
    backup_consumer_obj = None
    if not rqst_errors:
        matching_consumer_instances, consumer_instance, backup_consumer_obj = add_instance_using_validated_params(add_consumer_params, rqst_errors)

    return matching_consumer_instances, consumer_instance, backup_consumer_obj


def validate_add_instance_rqst_params(post_data, post_errors):
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
        if month:
            if month < 1 or month > 12:
                post_errors.append("Month must be between 1 and 12 inclusive")

        day = clean_int_value_from_dict_object(date_met_nav_dict, "date_met_nav", "Day", post_errors)
        if day:
            if day < 1 or day > 31:
                post_errors.append("Day must be between 1 and 31 inclusive")

        year = clean_int_value_from_dict_object(date_met_nav_dict, "date_met_nav", "Year", post_errors)
        if year:
            if year < 1 or year > 9999:
                post_errors.append("Year must be between 1 and 9999 inclusive")

        if not post_errors:
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
    rqst_cps_info_dict = clean_dict_value_from_dict_object(post_data,
                                                           "root",
                                                           "cps_info",
                                                           post_errors,
                                                           no_key_allowed=True,
                                                           none_allowed=True)
    if rqst_cps_consumer and not rqst_cps_info_dict:
        post_errors.append("cps_info key must be present and a non empty dictionary in order to set cps_consumer to True.")

    validated_cps_info_dict = None
    if rqst_cps_info_dict:
        if rqst_cps_consumer:
            validated_cps_info_dict = validate_cps_info_params_for_add_instance_rqst(rqst_cps_info_dict, rqst_consumer_met_nav_at, rqst_consumer_household_size, nav_instance, post_errors)
        else:
            post_errors.append("cps_consumer key must be True in order to add consumer with cps_info.")

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
        consumer_entry_query = PICConsumer.objects.filter(first_name=rqst_dependent_f_name,
                                                          last_name=rqst_dependent_l_name)
        for consumer_entry in consumer_entry_query:
            found_consumer_entries.append(consumer_entry.id)

    return found_consumer_entries


def validate_rqst_params_and_modify_instance(rqst_params, post_errors):
    validated_params = validate_modify_instance_rqst_params(rqst_params, post_errors)

    consumer_instance = None
    backup_consumer_obj = None
    if not post_errors:
        consumer_instance, backup_consumer_obj = modify_instance_using_validated_params(validated_params, post_errors)

    return consumer_instance, backup_consumer_obj


def validate_modify_instance_rqst_params(rqst_params, rqst_errors):
    validated_params = {}

    consumer_instance = None
    rqst_consumer_id = clean_int_value_from_dict_object(rqst_params, "root", "Consumer Database ID", rqst_errors)
    validated_params['rqst_consumer_id'] = rqst_consumer_id
    if not rqst_errors:
        try:
            consumer_instance = PICConsumer.objects.get(id=rqst_consumer_id)
        except PICConsumer.DoesNotExist:
            rqst_errors.append('Consumer database entry does not exist for the id: {}'.format(rqst_consumer_id))
    validated_params['consumer_instance'] = consumer_instance

    if "Email" in rqst_params:
        rqst_consumer_email = clean_string_value_from_dict_object(rqst_params, "root", "Email", rqst_errors,
                                                                  empty_string_allowed=True)
        if rqst_consumer_email:
            try:
                validate_email(rqst_consumer_email)
            except forms.ValidationError:
                rqst_errors.append("{!s} must be a valid email address".format(rqst_consumer_email))

        validated_params["rqst_consumer_email"] = rqst_consumer_email
    if "First Name" in rqst_params:
        rqst_consumer_f_name = clean_string_value_from_dict_object(rqst_params, "root", "First Name", rqst_errors)

        validated_params["rqst_consumer_f_name"] = rqst_consumer_f_name
    if "Middle Name" in rqst_params:
        rqst_consumer_m_name = clean_string_value_from_dict_object(rqst_params, "root", "Middle Name", rqst_errors,
                                                                   empty_string_allowed=True)

        validated_params["rqst_consumer_m_name"] = rqst_consumer_m_name
    if "Last Name" in rqst_params:
        rqst_consumer_l_name = clean_string_value_from_dict_object(rqst_params, "root", "Last Name", rqst_errors)

        validated_params["rqst_consumer_l_name"] = rqst_consumer_l_name
    if "Plan" in rqst_params:
        rqst_consumer_plan = clean_string_value_from_dict_object(rqst_params, "root", "Plan", rqst_errors,
                                                                 empty_string_allowed=True)

        validated_params["rqst_consumer_plan"] = rqst_consumer_plan
    rqst_consumer_met_nav_at = None
    if "Met Navigator At" in rqst_params:
        rqst_consumer_met_nav_at = clean_string_value_from_dict_object(rqst_params, "root", "Met Navigator At", rqst_errors)

        validated_params["rqst_consumer_met_nav_at"] = rqst_consumer_met_nav_at
    rqst_consumer_household_size = None
    if "Household Size" in rqst_params:
        rqst_consumer_household_size = clean_int_value_from_dict_object(rqst_params, "root", "Household Size", rqst_errors)

        validated_params["rqst_consumer_household_size"] = rqst_consumer_household_size
    if "Phone Number" in rqst_params:
        rqst_consumer_phone = clean_string_value_from_dict_object(rqst_params, "root", "Phone Number", rqst_errors,
                                                                  empty_string_allowed=True)

        validated_params["rqst_consumer_phone"] = rqst_consumer_phone
    if "Preferred Language" in rqst_params:
        rqst_consumer_pref_lang = clean_string_value_from_dict_object(rqst_params, "root", "Preferred Language",
                                                                      rqst_errors, empty_string_allowed=True)
        validated_params["rqst_consumer_pref_lang"] = rqst_consumer_pref_lang
    if "Navigator Notes" in rqst_params:
        rqst_navigator_notes = clean_list_value_from_dict_object(rqst_params, "root", "Navigator Notes", rqst_errors,
                                                                 empty_list_allowed=True)

        validated_params["rqst_navigator_notes"] = rqst_navigator_notes
    if "Address Line 1" in rqst_params:
        rqst_address_line_1 = clean_string_value_from_dict_object(rqst_params, "root", "Address Line 1", rqst_errors,
                                                                  empty_string_allowed=True)

        validated_params["rqst_address_line_1"] = rqst_address_line_1
    if "Address Line 2" in rqst_params:
        rqst_address_line_2 = clean_string_value_from_dict_object(rqst_params, "root", "Address Line 2", rqst_errors,
                                                                  empty_string_allowed=True)
        if rqst_address_line_2 is None:
            rqst_address_line_2 = ''

        validated_params["rqst_address_line_2"] = rqst_address_line_2
    if "City" in rqst_params:
        rqst_city = clean_string_value_from_dict_object(rqst_params, "root", "City", rqst_errors, empty_string_allowed=True)

        validated_params["rqst_city"] = rqst_city
    if "State" in rqst_params:
        rqst_state = clean_string_value_from_dict_object(rqst_params, "root", "State", rqst_errors, empty_string_allowed=True)

        validated_params["rqst_state"] = rqst_state
    if "Zipcode" in rqst_params:
        rqst_zipcode = clean_string_value_from_dict_object(rqst_params, "root", "Zipcode", rqst_errors, empty_string_allowed=True)

        validated_params["rqst_zipcode"] = rqst_zipcode
    nav_instance = None
    if "Navigator Database ID" in rqst_params:
        rqst_nav_id = clean_int_value_from_dict_object(rqst_params, "root", "Navigator Database ID", rqst_errors)
        if rqst_nav_id and not rqst_errors:
            try:
                nav_instance = PICStaff.objects.get(id=rqst_nav_id)
            except PICStaff.DoesNotExist:
                rqst_errors.append('Staff database entry does not exist for the navigator id: {}'.format(rqst_nav_id))

        validated_params["rqst_nav_id"] = rqst_nav_id
        validated_params["nav_instance"] = nav_instance
    rqst_date_met_nav = None
    if "date_met_nav" in rqst_params:
        date_met_nav_dict = clean_dict_value_from_dict_object(rqst_params, "root", "date_met_nav", rqst_errors,
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
                rqst_date_met_nav = datetime.date(year, month, day)

        validated_params["rqst_date_met_nav"] = rqst_date_met_nav
    if "cps_consumer" in rqst_params:
        rqst_cps_consumer = clean_bool_value_from_dict_object(rqst_params,
                                                              "root",
                                                              "cps_consumer",
                                                              rqst_errors,
                                                              no_key_allowed=True)

        validated_params["rqst_cps_consumer"] = rqst_cps_consumer
    if "cps_info" in rqst_params:
        rqst_cps_info_dict = clean_dict_value_from_dict_object(rqst_params,
                                                               "root",
                                                               "cps_info",
                                                               rqst_errors,
                                                               none_allowed=True)
        validated_cps_info_dict = None
        if consumer_instance and rqst_cps_info_dict:
            validated_cps_info_dict = validate_cps_info_params_for_modify_instance_rqst(rqst_cps_info_dict, consumer_instance, rqst_consumer_met_nav_at, rqst_consumer_household_size, nav_instance, rqst_errors)

        validated_params["rqst_cps_info_dict"] = rqst_cps_info_dict
        validated_params["validated_cps_info_dict"] = validated_cps_info_dict
    if "create_backup" in rqst_params:
        validated_params['rqst_create_backup'] = clean_bool_value_from_dict_object(rqst_params,
                                                                                   "root",
                                                                                   "create_backup",
                                                                                   rqst_errors,
                                                                                   no_key_allowed=True)
    if len(validated_params) < 3:
        rqst_errors.append("No parameters to modify are given.")

    return validated_params


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


def validate_rqst_params_and_delete_instance(post_data, post_errors):
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

    backup_consumer_obj = None
    if not post_errors:
        backup_consumer_obj = delete_instance_using_validated_params(rqst_consumer_id, rqst_create_backup, post_errors)

    return backup_consumer_obj
