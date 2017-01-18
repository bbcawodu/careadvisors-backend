"""
Defines utility functions and classes for consumer views
"""

import datetime
import math
import json
from .base import clean_string_value_from_dict_object
from .base import clean_int_value_from_dict_object
from .base import clean_list_value_from_dict_object
from .base import clean_dict_value_from_dict_object
from .base import clean_bool_value_from_dict_object
from picmodels.models import PICStaff
from picmodels.models import PICConsumer
from picmodels.models import ConsumerNote
from picmodels.models import Address
from picmodels.models import Country
from picmodels.models import ConsumerCPSInfoEntry
from picmodels.models import NavMetricsLocation
from django.db import IntegrityError
from django.core.validators import validate_email
from django import forms


def add_consumer(response_raw_data, post_data, post_errors):
    rqst_consumer_email = clean_string_value_from_dict_object(post_data, "root", "Email", post_errors, empty_string_allowed=True)
    if rqst_consumer_email and not post_errors:
        try:
            validate_email(rqst_consumer_email)
        except forms.ValidationError:
            post_errors.append("{!s} must be a valid email address".format(rqst_consumer_email))
    rqst_consumer_f_name = clean_string_value_from_dict_object(post_data, "root", "First Name", post_errors)
    rqst_consumer_m_name = clean_string_value_from_dict_object(post_data, "root", "Middle Name", post_errors, empty_string_allowed=True)
    rqst_consumer_l_name = clean_string_value_from_dict_object(post_data, "root", "Last Name", post_errors)
    rqst_consumer_plan = clean_string_value_from_dict_object(post_data, "root", "Plan", post_errors, empty_string_allowed=True)
    rqst_consumer_met_nav_at = clean_string_value_from_dict_object(post_data, "root", "Met Navigator At", post_errors)
    rqst_consumer_household_size = clean_int_value_from_dict_object(post_data, "root", "Household Size", post_errors)
    rqst_consumer_phone = clean_string_value_from_dict_object(post_data, "root", "Phone Number", post_errors, empty_string_allowed=True)
    rqst_consumer_pref_lang = clean_string_value_from_dict_object(post_data, "root", "Preferred Language", post_errors, empty_string_allowed=True)
    rqst_navigator_notes = clean_list_value_from_dict_object(post_data, "root", "Navigator Notes", post_errors, empty_list_allowed=True)
    rqst_nav_id = clean_int_value_from_dict_object(post_data, "root", "Navigator Database ID", post_errors)

    rqst_address_line_1 = clean_string_value_from_dict_object(post_data, "root", "Address Line 1", post_errors, empty_string_allowed=True)
    rqst_address_line_2 = clean_string_value_from_dict_object(post_data, "root", "Address Line 2", post_errors, empty_string_allowed=True)
    if rqst_address_line_2 is None:
        rqst_address_line_2 = ''
    rqst_city = clean_string_value_from_dict_object(post_data, "root", "City", post_errors, empty_string_allowed=True)
    rqst_state = clean_string_value_from_dict_object(post_data, "root", "State", post_errors, empty_string_allowed=True)
    rqst_zipcode = clean_string_value_from_dict_object(post_data, "root", "Zipcode", post_errors, empty_string_allowed=True)

    date_met_nav_dict = clean_dict_value_from_dict_object(post_data, "root", "date_met_nav", post_errors, none_allowed=True)
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
    if not rqst_cps_consumer:
        rqst_cps_consumer = False

    if rqst_cps_consumer:
        rqst_cps_info_dict = clean_dict_value_from_dict_object(post_data,
                                                               "root",
                                                               "cps_info",
                                                               post_errors,
                                                               no_key_allowed=True)

    if len(post_errors) == 0:
        address_instance = None
        if rqst_address_line_1 != '' and rqst_city != '' and rqst_state != '' and rqst_zipcode != '':
            address_instance, address_instance_created = Address.objects.get_or_create(address_line_1=rqst_address_line_1,
                                                                                       address_line_2=rqst_address_line_2,
                                                                                       city=rqst_city,
                                                                                       state_province=rqst_state,
                                                                                       zipcode=rqst_zipcode,
                                                                                       country=Country.objects.all()[0])

        consumer_rqst_values = {"email": rqst_consumer_email,
                                "middle_name": rqst_consumer_m_name,
                                "phone": rqst_consumer_phone,
                                "plan": rqst_consumer_plan,
                                "preferred_language": rqst_consumer_pref_lang,
                                "address": address_instance,
                                "date_met_nav": rqst_date_met_nav,}

        try:
            consumer_instance, consumer_instance_created = PICConsumer.objects.get_or_create(first_name=rqst_consumer_f_name,
                                                                                             last_name=rqst_consumer_l_name,
                                                                                             met_nav_at=rqst_consumer_met_nav_at,
                                                                                             household_size=rqst_consumer_household_size,
                                                                                             defaults=consumer_rqst_values)
            if not consumer_instance_created:
                query_params = {"first_name":rqst_consumer_f_name,
                                 "last_name":rqst_consumer_l_name,
                                 "met_nav_at":rqst_consumer_met_nav_at,
                                 "household_size":rqst_consumer_household_size,}
                post_errors.append('Consumer database entry already exists for the parameters: {!s}'.format(json.dumps(query_params)))
            else:
                try:
                    nav_instance = PICStaff.objects.get(id=rqst_nav_id)
                    consumer_instance.navigator = nav_instance
                    consumer_instance.save()
                except PICStaff.DoesNotExist:
                    consumer_instance.delete()
                    consumer_instance = None
                    post_errors.append('Staff database entry does not exist for the navigator id: {!s}'.format(str(rqst_nav_id)))

                if consumer_instance:
                    old_consumer_notes = ConsumerNote.objects.filter(consumer=consumer_instance.id)
                    for old_consumer_note in old_consumer_notes:
                        old_consumer_note.delete()

                    for navigator_note in rqst_navigator_notes:
                        consumer_note_object = ConsumerNote(consumer=consumer_instance, navigator_notes=navigator_note)
                        consumer_note_object.save()

                    if rqst_cps_consumer:
                        add_cps_info_to_consumer_instance(response_raw_data, consumer_instance, rqst_cps_info_dict, post_errors)
                    else:
                        response_raw_data['Status']['Warnings'].append('Consumer instance created without cps_info')

        except IntegrityError:
            query_params = {"first_name":rqst_consumer_f_name,
                             "last_name":rqst_consumer_l_name,
                             "met_nav_at":rqst_consumer_met_nav_at,
                             "household_size":rqst_consumer_household_size,}
            post_errors.append('Consumer database entry already exists for the parameters: {!s}'.format(json.dumps(query_params)))
            consumer_instance = PICConsumer.objects.get(email=rqst_consumer_email)
        response_raw_data['Data'] = {"Database ID": consumer_instance.id}

    return response_raw_data


def add_cps_info_to_consumer_instance(response_raw_data, consumer_instance, rqst_cps_info_dict, post_errors):
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
            primary_dependent_found_PICConsumer_entries = check_consumer_entries_for_dependent_info(rqst_primary_dependent_dict, post_errors)
            if not primary_dependent_found_PICConsumer_entries:
                try:
                    primary_dependent_object = PICConsumer(first_name=rqst_primary_dependent_dict["first_name"],
                                                           last_name=rqst_primary_dependent_dict["last_name"],
                                                           met_nav_at=consumer_instance.met_nav_at,
                                                           household_size=consumer_instance.household_size,
                                                           navigator=consumer_instance.navigator
                                                           )
                except PICConsumer.IntegrityError:
                    post_errors.append("Error creating primary_dependent database entry for params: {!s}".format(json.dumps(rqst_primary_dependent_dict)))
            else:
                post_errors.append("The following PICConsumer objects were found for given primary_dependent: {!s}".format(json.dumps(primary_dependent_found_PICConsumer_entries)))
        else:
            try:
                primary_dependent_object = PICConsumer.objects.get(id=rqst_primary_dependent_database_id)
            except NavMetricsLocation.DoesNotExists:
                post_errors.append("PICConsumer object does not exist for primary_dependent Database ID: {!s}".format(str(rqst_primary_dependent_database_id)))

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
        for rqst_secondary_dependent_dict in rqst_secondary_dependents:
            secondary_dependent_object = None
            if len(post_errors) == 0:
                rqst_secondary_dependent_database_id = clean_int_value_from_dict_object(rqst_secondary_dependent_dict,
                                                                                        "secondary_dependent",
                                                                                        "Consumer Database ID",
                                                                                        post_errors,
                                                                                        no_key_allowed=True)
                if not rqst_secondary_dependent_database_id:
                    secondary_dependent_found_PICConsumer_entries = check_consumer_entries_for_dependent_info(
                        rqst_secondary_dependent_dict, post_errors)
                    if not secondary_dependent_found_PICConsumer_entries:
                        try:
                            secondary_dependent_object = PICConsumer(first_name=rqst_secondary_dependent_dict["first_name"],
                                                                     last_name=rqst_secondary_dependent_dict["last_name"],
                                                                     met_nav_at=consumer_instance.met_nav_at,
                                                                     household_size=consumer_instance.household_size,
                                                                     navigator=consumer_instance.navigator)
                        except PICConsumer.IntegrityError:
                            post_errors.append(
                                "Error creating secondary_dependent database entry for params: {!s}".format(
                                    json.dumps(rqst_secondary_dependent_dict)))
                    else:
                        post_errors.append(
                            "The following PICConsumer objects were found for given secondary_dependent: {!s}".format(
                                json.dumps(secondary_dependent_found_PICConsumer_entries)))
                else:
                    try:
                        secondary_dependent_object = PICConsumer.objects.get(id=rqst_secondary_dependent_database_id)
                    except NavMetricsLocation.DoesNotExists:
                        post_errors.append(
                            "PICConsumer object does not exist for secondary_dependent Database ID: {!s}".format(
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
    if len(post_errors) == 0:
        cps_info_object = ConsumerCPSInfoEntry(consumer=consumer_instance)

        try:
            cps_location_object = NavMetricsLocation.objects.get(name=rqst_cps_location)
            if not cps_location_object.cps_location:
                post_errors.append("{!s} is not a cps_location".format(rqst_cps_location))
            else:
                cps_info_object.cps_location = cps_location_object
        except NavMetricsLocation.DoesNotExists:
            post_errors.append("NavMetricsLocation object does not exist for name: {!s}".format(rqst_cps_location))

        cps_info_object.apt_date = rqst_apt_date
        cps_info_object.target_list = rqst_target_list
        cps_info_object.phone_apt = rqst_phone_apt
        cps_info_object.case_mgmt_type = rqst_case_mgmt_type
        cps_info_object.case_mgmt_type = rqst_case_mgmt_type

        cps_info_object.case_mgmt_status = rqst_case_mgmt_status
        if not cps_info_object.check_case_mgmt_status_choices():
            post_errors.append("case_mgmt_status: {!s} is not a valid choice".format(cps_info_object.case_mgmt_status))
        cps_info_object.app_type = rqst_app_type
        if not cps_info_object.check_app_type_choices():
            post_errors.append("app_type: {!s} is not a valid choice".format(cps_info_object.app_type))
        cps_info_object.app_status = rqst_app_status
        if not cps_info_object.check_app_status_choices():
            post_errors.append("app_status: {!s} is not a valid choice".format(cps_info_object.app_status))

        if len(post_errors) == 0:
            consumer_instance.cps_consumer = True
            consumer_instance.save()

            if primary_dependent_object._state.adding:
                primary_dependent_object.save()
            cps_info_object.primary_dependent = primary_dependent_object

            cps_info_object.save()

            if secondary_dependents_list:
                for secondary_dependent_instance in secondary_dependents_list:
                    if secondary_dependent_instance._state.adding:
                        secondary_dependent_instance.save()
                cps_info_object.secondary_dependents = secondary_dependents_list
        else:
            consumer_instance.delete()
    else:
        consumer_instance.delete()


def check_consumer_entries_for_dependent_info(rqst_primary_dependent_dict, post_errors):
    found_consumer_entries = []

    rqst_dependent_f_name = clean_string_value_from_dict_object(rqst_primary_dependent_dict,
                                                                "primary_dependent",
                                                                "first_name",
                                                                post_errors)
    rqst_dependent_l_name = clean_string_value_from_dict_object(rqst_primary_dependent_dict,
                                                                "primary_dependent",
                                                                "last_name",
                                                                post_errors)

    if len(post_errors) == 0:
        consumer_entry_query = PICConsumer.objects.filter(first_name=rqst_dependent_f_name,
                                                          last_name=rqst_dependent_l_name)
        for consumer_entry in consumer_entry_query:
            found_consumer_entries.append(consumer_entry.id)

    return found_consumer_entries


def modify_consumer(response_raw_data, post_data, post_errors):
    rqst_consumer_email = clean_string_value_from_dict_object(post_data, "root", "Email", post_errors, empty_string_allowed=True)
    rqst_consumer_f_name = clean_string_value_from_dict_object(post_data, "root", "First Name", post_errors)
    rqst_consumer_m_name = clean_string_value_from_dict_object(post_data, "root", "Middle Name", post_errors, empty_string_allowed=True)
    rqst_consumer_l_name = clean_string_value_from_dict_object(post_data, "root", "Last Name", post_errors)
    rqst_consumer_plan = clean_string_value_from_dict_object(post_data, "root", "Plan", post_errors, empty_string_allowed=True)
    rqst_consumer_met_nav_at = clean_string_value_from_dict_object(post_data, "root", "Met Navigator At", post_errors)
    rqst_consumer_household_size = clean_int_value_from_dict_object(post_data, "root", "Household Size", post_errors)
    rqst_consumer_phone = clean_string_value_from_dict_object(post_data, "root", "Phone Number", post_errors, empty_string_allowed=True)
    rqst_consumer_pref_lang = clean_string_value_from_dict_object(post_data, "root", "Preferred Language", post_errors, empty_string_allowed=True)
    rqst_navigator_notes = clean_list_value_from_dict_object(post_data, "root", "Navigator Notes", post_errors, empty_list_allowed=True)
    rqst_nav_id = clean_int_value_from_dict_object(post_data, "root", "Navigator Database ID", post_errors)
    rqst_consumer_id = clean_int_value_from_dict_object(post_data, "root", "Consumer Database ID", post_errors)

    rqst_address_line_1 = clean_string_value_from_dict_object(post_data, "root", "Address Line 1", post_errors, empty_string_allowed=True)
    rqst_address_line_2 = clean_string_value_from_dict_object(post_data, "root", "Address Line 2", post_errors, empty_string_allowed=True)
    if rqst_address_line_2 is None:
        rqst_address_line_2 = ''
    rqst_city = clean_string_value_from_dict_object(post_data, "root", "City", post_errors, empty_string_allowed=True)
    rqst_state = clean_string_value_from_dict_object(post_data, "root", "State", post_errors, empty_string_allowed=True)
    rqst_zipcode = clean_string_value_from_dict_object(post_data, "root", "Zipcode", post_errors, empty_string_allowed=True)

    date_met_nav_dict = clean_dict_value_from_dict_object(post_data, "root", "date_met_nav", post_errors, none_allowed=True)
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

    if len(post_errors) == 0:
        address_instance = None
        if rqst_address_line_1 != '' and rqst_city != '' and rqst_state != '' and rqst_zipcode != '':
            address_instance, address_instance_created = Address.objects.get_or_create(address_line_1=rqst_address_line_1,
                                                                                       address_line_2=rqst_address_line_2,
                                                                                       city=rqst_city,
                                                                                       state_province=rqst_state,
                                                                                       zipcode=rqst_zipcode,
                                                                                       country=Country.objects.all()[0])

        try:
            consumer_instance = PICConsumer.objects.get(id=rqst_consumer_id)
            consumer_instance.first_name = rqst_consumer_f_name
            consumer_instance.middle_name = rqst_consumer_m_name
            consumer_instance.last_name = rqst_consumer_l_name
            consumer_instance.phone = rqst_consumer_phone
            consumer_instance.address = address_instance
            consumer_instance.plan = rqst_consumer_plan
            consumer_instance.met_nav_at = rqst_consumer_met_nav_at
            consumer_instance.household_size = rqst_consumer_household_size
            consumer_instance.preferred_language = rqst_consumer_pref_lang
            consumer_instance.email = rqst_consumer_email
            consumer_instance.date_met_nav = rqst_date_met_nav

            nav_instance = PICStaff.objects.get(id=rqst_nav_id)
            consumer_instance.navigator = nav_instance

            consumer_instance.save()

            if consumer_instance:
                old_consumer_notes = ConsumerNote.objects.filter(consumer=consumer_instance.id)
                for old_consumer_note in old_consumer_notes:
                    old_consumer_note.delete()

                for navigator_note in rqst_navigator_notes:
                    consumer_note_object = ConsumerNote(consumer=consumer_instance, navigator_notes=navigator_note)
                    consumer_note_object.save()

            response_raw_data['Data'] = {"Database ID": consumer_instance.id}
        except PICConsumer.DoesNotExist:
            post_errors.append('Consumer database entry does not exist for the id: {!s}'.format(str(rqst_consumer_id)))
        except PICConsumer.MultipleObjectsReturned:
            post_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_consumer_id)))
        except IntegrityError:
            post_errors.append('Database entry already exists for the id: {!s}'.format(str(rqst_consumer_id)))
        except PICStaff.DoesNotExist:
            post_errors.append('Staff database entry does not exist for the navigator id: {!s}'.format(str(rqst_nav_id)))

    return response_raw_data


def delete_consumer(response_raw_data, post_data, post_errors):
    rqst_consumer_id = clean_int_value_from_dict_object(post_data, "root", "Consumer Database ID", post_errors)

    if len(post_errors) == 0:
        try:
            consumer_instance = PICConsumer.objects.get(id=rqst_consumer_id)
            consumer_instance.delete()
            response_raw_data['Data'] = {"Database ID": "Deleted"}
        except PICConsumer.DoesNotExist:
            post_errors.append('Consumer database entry does not exist for the id: {!s}'.format(str(rqst_consumer_id)))
        except PICConsumer.MultipleObjectsReturned:
            post_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_consumer_id)))

    return response_raw_data


def retrieve_f_l_name_consumers(response_raw_data, rqst_errors, consumers, rqst_first_name, rqst_last_name):
    consumers = consumers.filter(first_name__iexact=rqst_first_name, last_name__iexact=rqst_last_name)
    if len(consumers) > 0:
        consumer_dict = {}
        rqst_full_name = rqst_first_name + " " + rqst_last_name
        for consumer in consumers:
            if rqst_full_name not in consumer_dict:
                consumer_dict[rqst_full_name] = [consumer.return_values_dict()]
            else:
                consumer_dict[rqst_full_name].append(consumer.return_values_dict())

        consumer_list = []
        for consumer_key, consumer_entry in consumer_dict.items():
            consumer_list.append(consumer_entry)
        response_raw_data["Data"] = consumer_list
    else:
        rqst_errors.append('Consumer with name: {!s} {!s} not found in database'.format(rqst_first_name,
                                                                                            rqst_last_name))

    return response_raw_data, rqst_errors


def retrieve_email_consumers(response_raw_data, rqst_errors, consumers, rqst_email, list_of_emails):
    consumer_dict = {}
    consumers_object = consumers
    for email in list_of_emails:
        consumers = consumers_object.filter(email__iexact=email)
        for consumer in consumers:
            if email not in consumer_dict:
                consumer_dict[email] = [consumer.return_values_dict()]
            else:
                consumer_dict[email].append(consumer.return_values_dict())
    if len(consumer_dict) > 0:
        consumer_list = []
        for consumer_key, consumer_entry in consumer_dict.items():
            consumer_list.append(consumer_entry)
        response_raw_data["Data"] = consumer_list
        for email in list_of_emails:
            if email not in consumer_dict:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Consumer with email: {!s} not found in database'.format(email))
    else:
        rqst_errors.append('Consumer with emails(s): {!s} not found in database'.format(rqst_email))

    return response_raw_data, rqst_errors


def retrieve_first_name_consumers(response_raw_data, rqst_errors, consumers, rqst_first_name, list_of_first_names):
    consumer_dict = {}
    consumers_object = consumers
    for first_name in list_of_first_names:
        consumers = consumers_object.filter(first_name__iexact=first_name)
        for consumer in consumers:
            if first_name not in consumer_dict:
                consumer_dict[first_name] = [consumer.return_values_dict()]
            else:
                consumer_dict[first_name].append(consumer.return_values_dict())
    if len(consumer_dict) > 0:
        consumer_list = []
        for consumer_key, consumer_entry in consumer_dict.items():
            consumer_list.append(consumer_entry)
        response_raw_data["Data"] = consumer_list
        for name in list_of_first_names:
            if name not in consumer_dict:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Consumer with first name: {!s} not found in database'.format(name))
    else:
        rqst_errors.append('Consumer with first name(s): {!s} not found in database'.format(rqst_first_name))

    return response_raw_data, rqst_errors


def retrieve_last_name_consumers(response_raw_data, rqst_errors, consumers, rqst_last_name, list_of_last_names):
    consumer_dict = {}
    consumers_object = consumers
    for last_name in list_of_last_names:
        consumers = consumers_object.filter(last_name__iexact=last_name)
        for consumer in consumers:
            if last_name not in consumer_dict:
                consumer_dict[last_name] = [consumer.return_values_dict()]
            else:
                consumer_dict[last_name].append(consumer.return_values_dict())
    if len(consumer_dict) > 0:
        consumer_list = []
        for consumer_key, consumer_entry in consumer_dict.items():
            consumer_list.append(consumer_entry)
        response_raw_data["Data"] = consumer_list
        for name in list_of_last_names:
            if name not in consumer_dict:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Staff Member with last name: {!s} not found in database'.format(name))
    else:
        rqst_errors.append('Staff Member with last name(s): {!s} not found in database'.format(rqst_last_name))

    return response_raw_data, rqst_errors


def retrieve_id_consumers(response_raw_data, rqst_errors, consumers, rqst_consumer_id, list_of_ids):
    if rqst_consumer_id == "all":
        all_consumers = consumers
        consumer_dict = {}
        for consumer in all_consumers:
            consumer_dict[consumer.id] = consumer.return_values_dict()
        consumer_list = []
        for consumer_key, consumer_entry in consumer_dict.items():
            consumer_list.append(consumer_entry)

        response_raw_data["Data"] = consumer_list
    elif list_of_ids:
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            consumers = consumers.filter(id__in=list_of_ids)
            if len(consumers) > 0:

                consumer_dict = {}
                for consumer in consumers:
                    consumer_dict[consumer.id] = consumer.return_values_dict()
                consumer_list = []
                for consumer_key, consumer_entry in consumer_dict.items():
                    consumer_list.append(consumer_entry)
                response_raw_data["Data"] = consumer_list

                for consumer_id in list_of_ids:
                    if consumer_id not in consumer_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Consumer with id: {!s} not found in database'.format(str(consumer_id)))
            else:
                rqst_errors.append('No consumers found for database ID(s): ' + rqst_consumer_id)
        else:
            rqst_errors.append('No valid consumer IDs provided in request (must be integers)')

    return response_raw_data, rqst_errors


def break_results_into_pages(request, response_raw_data, CONSUMERS_PER_PAGE, rqst_page_no):
    consumer_list = response_raw_data["Data"]
    if len(consumer_list) > CONSUMERS_PER_PAGE:
        if rqst_page_no:
            if len(consumer_list) > ((rqst_page_no - 1) * CONSUMERS_PER_PAGE):
                for i, consumer in enumerate(consumer_list[:(CONSUMERS_PER_PAGE * (rqst_page_no - 1))]):
                    consumer_list[i] = consumer["Database ID"]
            if len(consumer_list) > (rqst_page_no * CONSUMERS_PER_PAGE):
                for i, consumer in enumerate(consumer_list[(rqst_page_no * CONSUMERS_PER_PAGE):]):
                    consumer_list[(rqst_page_no * CONSUMERS_PER_PAGE)+i] = consumer["Database ID"]
        else:
            response_raw_data["Page URLs"] = []
            total_pages = math.ceil(len(consumer_list) / CONSUMERS_PER_PAGE)
            for i in range(total_pages):
                response_raw_data["Page URLs"].append(request.build_absolute_uri(None) + "&page=" + str(i+1))

            for i, consumer in enumerate(consumer_list[CONSUMERS_PER_PAGE:]):
                consumer_list[CONSUMERS_PER_PAGE+i] = consumer["Database ID"]

    response_raw_data["Data"] = consumer_list
    return response_raw_data
