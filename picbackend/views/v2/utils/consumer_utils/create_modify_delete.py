"""
Defines utility functions and classes for consumer views
"""

import datetime
import json
from ..base import clean_string_value_from_dict_object
from ..base import clean_int_value_from_dict_object
from ..base import clean_list_value_from_dict_object
from ..base import clean_dict_value_from_dict_object
from ..base import clean_bool_value_from_dict_object
from picmodels.models import PICStaff
from picmodels.models import PICConsumer
from picmodels.models import PICConsumerBackup
from picmodels.models import ConsumerNote
from picmodels.models import Address
from picmodels.models import Country
from picmodels.models import ConsumerCPSInfoEntry
from picmodels.models import NavMetricsLocation
from django.db import IntegrityError
from django.core.validators import validate_email
from django import forms


def add_consumer_using_api_rqst_params(response_raw_data, rqst_consumer_info, post_errors):
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

    if len(post_errors) == 0:
        found_consumers = PICConsumer.objects.filter(first_name=add_consumer_params['rqst_consumer_f_name'],
                                                     last_name=add_consumer_params['rqst_consumer_l_name'])

        if found_consumers and not add_consumer_params['force_create_consumer']:
            query_params = {"first_name": add_consumer_params['rqst_consumer_f_name'],
                            "last_name": add_consumer_params['rqst_consumer_l_name'], }
            post_errors.append('Consumer database entry(s) already exists for the parameters: {!s}'.format(
                json.dumps(query_params)))

            response_raw_data['Data']['Possible Consumer Matches'] = []
            for consumer in found_consumers:
                response_raw_data['Data']['Possible Consumer Matches'].append(consumer.return_values_dict())
        else:
            consumer_instance, backup_consumer_obj = create_consumer_obj(add_consumer_params, post_errors)

            if len(post_errors) == 0:
                if consumer_instance:
                    response_raw_data['Data']["Database ID"] = consumer_instance.id
                if backup_consumer_obj:
                    response_raw_data['Data']["backup_consumer"] = backup_consumer_obj.return_values_dict()

    return response_raw_data


def create_consumer_obj(consumer_params, post_errors):
    address_instance = None
    if consumer_params['rqst_address_line_1'] != '' and consumer_params['rqst_city'] != '' and \
                    consumer_params['rqst_state'] != '' and consumer_params['rqst_zipcode'] != '':
        address_instance, address_instance_created = Address.objects.get_or_create(
            address_line_1=consumer_params['rqst_address_line_1'],
            address_line_2=consumer_params['rqst_address_line_2'],
            city=consumer_params['rqst_city'],
            state_province=consumer_params['rqst_state'],
            zipcode=consumer_params['rqst_zipcode'],
            country=Country.objects.all()[0])

    consumer_instance = None
    backup_consumer_obj = None

    try:
        nav_instance = PICStaff.objects.get(id=consumer_params['rqst_nav_id'])
        consumer_instance = PICConsumer(first_name=consumer_params['rqst_consumer_f_name'],
                                        middle_name=consumer_params['rqst_consumer_m_name'],
                                        last_name=consumer_params['rqst_consumer_l_name'],
                                        email=consumer_params['rqst_consumer_email'],
                                        phone=consumer_params['rqst_consumer_phone'],
                                        plan=consumer_params['rqst_consumer_plan'],
                                        preferred_language=consumer_params['rqst_consumer_pref_lang'],
                                        address=address_instance,
                                        date_met_nav=consumer_params['rqst_date_met_nav'],
                                        met_nav_at=consumer_params['rqst_consumer_met_nav_at'],
                                        household_size=consumer_params['rqst_consumer_household_size'],
                                        )
        consumer_instance.navigator = nav_instance
        consumer_instance.save()

        for navigator_note in consumer_params['rqst_navigator_notes']:
            consumer_note_object = ConsumerNote(consumer=consumer_instance,
                                                navigator_notes=navigator_note)
            consumer_note_object.save()

        if consumer_params['rqst_cps_consumer']:
            add_cps_info_to_consumer_instance(consumer_instance, consumer_params['rqst_cps_info_dict'], post_errors)

        if len(post_errors) == 0 and consumer_params['rqst_create_backup']:
            backup_consumer_obj = create_backup_consumer_obj(consumer_instance)
    except PICStaff.DoesNotExist:
        post_errors.append('Staff database entry does not exist for the navigator id: {!s}'.format(
            str(consumer_params['rqst_nav_id'])))

    return consumer_instance, backup_consumer_obj


def add_cps_info_to_consumer_instance(consumer_instance, rqst_cps_info_dict, post_errors):
    """
    This function takes a consumer database instance and a dictionary populated with CPS consumer info, parses the info
    for errors, and adds the CPS to the consumer info if there are no errors.

    :param consumer_instance: (type: PICConsumer) PICConsumer instance to add CPS info to
    :param rqst_cps_info_dict: (type: dictionary) CPS info to parse
    :param post_errors: (type: list) list of error messages
    :return: None
    """

    cps_info_params = get_consumer_cps_info_put_params(rqst_cps_info_dict, consumer_instance, post_errors)

    if len(post_errors) == 0:
        cps_info_object = ConsumerCPSInfoEntry()

        rqst_cps_location = cps_info_params["rqst_cps_location"]
        try:
            cps_location_object = NavMetricsLocation.objects.get(name=rqst_cps_location)
            if not cps_location_object.cps_location:
                post_errors.append("{!s} is not a cps_location".format(rqst_cps_location))
            else:
                cps_info_object.cps_location = cps_location_object
        except NavMetricsLocation.DoesNotExist:
            post_errors.append("NavMetricsLocation object does not exist for name: {!s}".format(rqst_cps_location))

        cps_info_object.apt_date = cps_info_params["rqst_apt_date"]
        cps_info_object.target_list = cps_info_params["rqst_target_list"]
        cps_info_object.phone_apt = cps_info_params["rqst_phone_apt"]
        cps_info_object.case_mgmt_type = cps_info_params["rqst_case_mgmt_type"]

        cps_info_object.case_mgmt_status = cps_info_params["rqst_case_mgmt_status"]
        if not cps_info_object.check_case_mgmt_status_choices():
            post_errors.append("case_mgmt_status: {!s} is not a valid choice".format(cps_info_object.case_mgmt_status))
        cps_info_object.app_type = cps_info_params["rqst_app_type"]
        if not cps_info_object.check_app_type_choices():
            post_errors.append("app_type: {!s} is not a valid choice".format(cps_info_object.app_type))
        cps_info_object.app_status = cps_info_params["rqst_app_status"]
        if not cps_info_object.check_app_status_choices():
            post_errors.append("app_status: {!s} is not a valid choice".format(cps_info_object.app_status))

        if len(post_errors) == 0:
            consumer_instance.cps_consumer = True
            consumer_instance.save()

            primary_dependent_object = cps_info_params["primary_dependent_object"]
            if primary_dependent_object._state.adding:
                primary_dependent_object.save()
            cps_info_object.primary_dependent = primary_dependent_object
            cps_info_object.save()

            secondary_dependents_list = cps_info_params["secondary_dependents_list"]
            if secondary_dependents_list:
                for secondary_dependent_instance in secondary_dependents_list:
                    if secondary_dependent_instance._state.adding:
                        secondary_dependent_instance.save()
                cps_info_object.secondary_dependents = secondary_dependents_list
            cps_info_object.save()

            consumer_instance.cps_info = cps_info_object
            consumer_instance.save()
        else:
            consumer_instance.delete()
    else:
        consumer_instance.delete()


def get_consumer_cps_info_put_params(rqst_cps_info_dict, consumer_instance, post_errors):
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
                                                           met_nav_at=consumer_instance.met_nav_at,
                                                           household_size=consumer_instance.household_size,
                                                           navigator=consumer_instance.navigator
                                                           )
                except IntegrityError:
                    post_errors.append("Error creating primary_dependent database entry for params: {!s}".format(
                        json.dumps(rqst_primary_dependent_dict)))
            else:
                post_errors.append(
                    "The following PICConsumer objects were found for given primary_dependent: {!s}".format(
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
                                met_nav_at=consumer_instance.met_nav_at,
                                household_size=consumer_instance.household_size,
                                navigator=consumer_instance.navigator)
                        except IntegrityError:
                            post_errors.append(
                                "Error creating secondary_dependent database entry for params: {!s}".format(
                                    json.dumps(rqst_secondary_dependent_dict)))
                    else:
                        post_errors.append(
                            "The following PICConsumer objects were found for secondary_dependent with index({!s}): {!s}".format(
                                str(dependent_index),
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


def modify_consumer_using_api_rqst_params(response_raw_data, post_data, post_errors):
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

    if len(post_errors) == 0:
        consumer_instance, backup_consumer_obj = create_consumer_obj(modify_consumer_params, post_errors)

        if len(post_errors) == 0:
            if consumer_instance:
                response_raw_data['Data']["Database ID"] = consumer_instance.id
            if backup_consumer_obj:
                response_raw_data['Data']["backup_consumer"] = backup_consumer_obj.return_values_dict()

    return response_raw_data


def modify_consumer_obj(consumer_params, post_errors):
    consumer_instance = None
    backup_consumer_obj = None

    address_instance = None
    if consumer_params['rqst_address_line_1'] != '' and consumer_params['rqst_city'] != '' and \
                    consumer_params['rqst_state'] != '' and consumer_params['rqst_zipcode'] != '':
        address_instance, address_instance_created = Address.objects.get_or_create(
            address_line_1=consumer_params['rqst_address_line_1'],
            address_line_2=consumer_params['rqst_address_line_2'],
            city=consumer_params['rqst_city'],
            state_province=consumer_params['rqst_state'],
            zipcode=consumer_params['rqst_zipcode'],
            country=Country.objects.all()[0])

    try:
        consumer_instance = PICConsumer.objects.get(id=consumer_params['rqst_consumer_id'])
        consumer_instance.first_name = consumer_params['rqst_consumer_f_name']
        consumer_instance.middle_name = consumer_params['rqst_consumer_m_name']
        consumer_instance.last_name = consumer_params['rqst_consumer_l_name']
        consumer_instance.phone = consumer_params['rqst_consumer_phone']
        consumer_instance.address = address_instance
        consumer_instance.plan = consumer_params['rqst_consumer_plan']
        consumer_instance.met_nav_at = consumer_params['rqst_consumer_met_nav_at']
        consumer_instance.household_size = consumer_params['rqst_consumer_household_size']
        consumer_instance.preferred_language = consumer_params['rqst_consumer_pref_lang']
        consumer_instance.email = consumer_params['rqst_consumer_email']
        consumer_instance.date_met_nav = consumer_params['rqst_date_met_nav']

        nav_instance = PICStaff.objects.get(id=consumer_params['rqst_nav_id'])
        consumer_instance.navigator = nav_instance

        if consumer_params['rqst_cps_consumer'] is not None:
            consumer_instance.cps_consumer = consumer_params['rqst_cps_consumer']
            if consumer_params['rqst_cps_consumer']:
                modify_consumer_cps_info(consumer_instance, consumer_params['rqst_cps_info_dict'], post_errors)
            else:
                try:
                    consumer_cps_info = consumer_instance.cps_info
                    consumer_instance.cps_info.remove()
                    consumer_cps_info.delete()
                except ConsumerCPSInfoEntry.DoesNotExist:
                    pass
        else:
            pass

        if len(post_errors) == 0:
            consumer_instance.save()
            old_consumer_notes = ConsumerNote.objects.filter(consumer=consumer_instance.id)
            for old_consumer_note in old_consumer_notes:
                old_consumer_note.delete()

            for navigator_note in consumer_params['rqst_navigator_notes']:
                consumer_note_object = ConsumerNote(consumer=consumer_instance, navigator_notes=navigator_note)
                consumer_note_object.save()

            if consumer_params['rqst_create_backup']:
                backup_consumer_obj = create_backup_consumer_obj(consumer_instance)
    except PICConsumer.DoesNotExist:
        post_errors.append('Consumer database entry does not exist for the id: {!s}'.format(
            str(consumer_params['rqst_consumer_id'])))
    except PICConsumer.MultipleObjectsReturned:
        post_errors.append(
            'Multiple database entries exist for the id: {!s}'.format(str(consumer_params['rqst_consumer_id'])))
    except IntegrityError:
        post_errors.append(
            'Database entry already exists for the id: {!s}'.format(str(consumer_params['rqst_consumer_id'])))
    except PICStaff.DoesNotExist:
        post_errors.append('Staff database entry does not exist for the navigator id: {!s}'.format(
            str(consumer_params['rqst_nav_id'])))

    return consumer_instance, backup_consumer_obj


def modify_consumer_cps_info(consumer_instance, rqst_cps_info_dict, post_errors):
    """
    This function takes a consumer database instance and a dictionary populated with CPS consumer info, parses the info
    for errors, and modifies the CPS info for that consumer if there are no errors.

    :param consumer_instance: (type: PICConsumer) PICConsumer instance to add CPS info to
    :param rqst_cps_info_dict: (type: dictionary) CPS info to parse
    :param post_errors: (type: list) list of error messages
    :return: None
    """

    cps_info_params = get_consumer_cps_info_put_params(rqst_cps_info_dict, consumer_instance, post_errors)

    if len(post_errors) == 0:
        try:
            cps_info_object = consumer_instance.cps_info
        except ConsumerCPSInfoEntry.DoesNotExist:
            cps_info_object = ConsumerCPSInfoEntry()

        rqst_cps_location = cps_info_params["rqst_cps_location"]
        try:
            cps_location_object = NavMetricsLocation.objects.get(name=rqst_cps_location)
            if not cps_location_object.cps_location:
                post_errors.append("{!s} is not a cps_location".format(rqst_cps_location))
            else:
                cps_info_object.cps_location = cps_location_object
        except NavMetricsLocation.DoesNotExist:
            post_errors.append("NavMetricsLocation object does not exist for name: {!s}".format(rqst_cps_location))

        cps_info_object.apt_date = cps_info_params['rqst_apt_date']
        cps_info_object.target_list = cps_info_params['rqst_target_list']
        cps_info_object.phone_apt = cps_info_params['rqst_phone_apt']
        cps_info_object.case_mgmt_type = cps_info_params['rqst_case_mgmt_type']

        cps_info_object.case_mgmt_status = cps_info_params['rqst_case_mgmt_status']
        if not cps_info_object.check_case_mgmt_status_choices():
            post_errors.append("case_mgmt_status: {!s} is not a valid choice".format(cps_info_object.case_mgmt_status))
        cps_info_object.app_type = cps_info_params['rqst_app_type']
        if not cps_info_object.check_app_type_choices():
            post_errors.append("app_type: {!s} is not a valid choice".format(cps_info_object.app_type))
        cps_info_object.app_status = cps_info_params['rqst_app_status']
        if not cps_info_object.check_app_status_choices():
            post_errors.append("app_status: {!s} is not a valid choice".format(cps_info_object.app_status))

        if len(post_errors) == 0:
            consumer_instance.cps_consumer = True
            consumer_instance.save()

            primary_dependent_object = cps_info_params['primary_dependent_object']
            if primary_dependent_object._state.adding:
                primary_dependent_object.save()
            cps_info_object.primary_dependent = primary_dependent_object

            cps_info_object.save()

            secondary_dependents_list = cps_info_params['secondary_dependents_list']
            if cps_info_object.secondary_dependents:
                cps_info_object.secondary_dependents.clear()
            if secondary_dependents_list:
                for secondary_dependent_instance in secondary_dependents_list:
                    if secondary_dependent_instance._state.adding:
                        secondary_dependent_instance.save()
                cps_info_object.secondary_dependents = secondary_dependents_list

            cps_info_object.save()

            consumer_instance.cps_info = cps_info_object
            consumer_instance.save()


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
    rqst_nav_id = clean_int_value_from_dict_object(post_data, "root", "Navigator Database ID", post_errors)

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

    rqst_cps_consumer = clean_bool_value_from_dict_object(post_data,
                                                          "root",
                                                          "cps_consumer",
                                                          post_errors,
                                                          no_key_allowed=True)

    rqst_cps_info_dict = None
    if rqst_cps_consumer:
        rqst_cps_info_dict = clean_dict_value_from_dict_object(post_data,
                                                               "root",
                                                               "cps_info",
                                                               post_errors,
                                                               no_key_allowed=True)
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
            "rqst_address_line_1": rqst_address_line_1,
            "rqst_address_line_2": rqst_address_line_2,
            "rqst_city": rqst_city,
            "rqst_state": rqst_state,
            "rqst_zipcode": rqst_zipcode,
            "rqst_date_met_nav": rqst_date_met_nav,
            "rqst_cps_consumer": rqst_cps_consumer,
            "rqst_cps_info_dict": rqst_cps_info_dict,
            "rqst_create_backup": rqst_create_backup}


def delete_consumer_using_api_rqst_params(response_raw_data, post_data, post_errors):
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

    if len(post_errors) == 0:
        try:
            consumer_instance = PICConsumer.objects.get(id=rqst_consumer_id)
            response_raw_data['Data'] = {}

            if rqst_create_backup:
                backup_consumer_obj = create_backup_consumer_obj(consumer_instance)
                if backup_consumer_obj:
                    response_raw_data['Data']["backup_consumer"] = backup_consumer_obj.return_values_dict()

            consumer_instance.delete()
            response_raw_data['Data']["Database ID"] = "Deleted"
        except PICConsumer.DoesNotExist:
            post_errors.append('Consumer database entry does not exist for the id: {!s}'.format(str(rqst_consumer_id)))
        except PICConsumer.MultipleObjectsReturned:
            post_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_consumer_id)))

    return response_raw_data


# getattr(object, field_name)
# need to manually copy consumer notes
def create_backup_consumer_obj(consumer_instance):
    """
    This function takes a PICConsumer instance, creates a PICConsumerBackup instance with the same information as the
    given PICConsumer instance and returns the PICConsumerBackup instance.

    :param consumer_instance: (type: PICConsumer) PICConsumer instance to be copied
    :return: (type: PICConsumerBackup) copied PICConsumerBackup instance
    """

    consumer_instance_fields = consumer_instance._meta.get_fields()
    non_null_field_name_list = []
    for field in consumer_instance_fields:
        try:
            if getattr(consumer_instance, field.name) is not None and field.name != 'id':
                non_null_field_name_list.append(field.name)
        except AttributeError:
            pass

    backup_consumer_obj = PICConsumerBackup()
    for orig_field in non_null_field_name_list:
        orig_field_value = getattr(consumer_instance, orig_field)
        if orig_field == "cps_info":
            pass
        else:
            setattr(backup_consumer_obj, orig_field, orig_field_value)
    backup_consumer_obj.save()

    if "cps_info" in non_null_field_name_list:
        cps_info_copy = ConsumerCPSInfoEntry()
        cps_info_orig = getattr(consumer_instance, "cps_info")
        cps_info_orig_fields = cps_info_orig._meta.get_fields()

        for cps_info_orig_field in cps_info_orig_fields:
            try:
                cps_info_orig_field_value = getattr(cps_info_orig, cps_info_orig_field.name)

                if cps_info_orig_field.name == 'secondary_dependents':
                    # Need to implement something to copy secondary dependents, breaks if you omit this
                    pass
                elif cps_info_orig_field.name != 'id':
                    setattr(cps_info_copy, cps_info_orig_field.name, cps_info_orig_field_value)
            except AttributeError:
                pass
        cps_info_copy.save()

        setattr(backup_consumer_obj, "cps_info", cps_info_copy)
        backup_consumer_obj.save()

    orig_consumer_notes = ConsumerNote.objects.filter(consumer=consumer_instance.id)
    for consumer_note in orig_consumer_notes:
        consumer_note_copy_object = ConsumerNote(consumer_backup=backup_consumer_obj,
                                                 navigator_notes=consumer_note.navigator_notes)
        consumer_note_copy_object.save()

    return backup_consumer_obj