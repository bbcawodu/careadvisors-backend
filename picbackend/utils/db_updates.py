from django.http import HttpResponse
from django.db import models, IntegrityError
from picmodels.models import PICStaff, MetricsSubmission, PlanStat, PICConsumer, NavMetricsLocation, Country, ConsumerNote,\
    Address, CredentialsModel
import datetime, json, httplib2, pytz, dateutil.parser
from picbackend.utils.base import clean_json_string_input, clean_json_int_input, clean_dict_input, clean_list_input,\
    parse_and_log_errors
from googleapiclient.discovery import build


def add_nav_hub_location(response_raw_data, post_json, post_errors):
    rqst_location_name = clean_json_string_input(post_json, "root", "Location Name", post_errors)
    rqst_address_line_1 = clean_json_string_input(post_json, "root", "Address Line 1", post_errors)
    rqst_address_line_2 = clean_json_string_input(post_json, "root", "Address Line 2", post_errors, empty_string_allowed=True)
    if rqst_address_line_2 is None:
        rqst_address_line_2 = ''
    rqst_city = clean_json_string_input(post_json, "root", "City", post_errors)
    rqst_state = clean_json_string_input(post_json, "root", "State", post_errors)
    rqst_zipcode = clean_json_string_input(post_json, "root", "Zipcode", post_errors)
    rqst_country = clean_json_string_input(post_json, "root", "Country", post_errors)

    if len(post_errors) == 0:
        address_instance, address_instance_created = Address.objects.get_or_create(address_line_1=rqst_address_line_1,
                                                                                   address_line_2=rqst_address_line_2,
                                                                                   city=rqst_city,
                                                                                   state_province=rqst_state,
                                                                                   zipcode=rqst_zipcode,
                                                                                   country=Country.objects.get(name=rqst_country))

        try:
            location_instance = NavMetricsLocation.objects.get(name=rqst_location_name, address=address_instance)
            post_errors.append('Nav Hub Location database entry already exists for the name: {!s}'.format(rqst_location_name))
        except NavMetricsLocation.DoesNotExist:
            location_instance = NavMetricsLocation(name=rqst_location_name, address=address_instance)
            location_instance.save()

        response_raw_data['Data'] = {"Database ID": location_instance.id}

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    return response_raw_data


def modify_nav_hub_location(response_raw_data, post_json, post_errors):
    # rqst_location_id = clean_json_int_input(post_json, "root", "Database ID", post_errors)
    rqst_location_name = clean_json_string_input(post_json, "root", "Location Name", post_errors)
    rqst_address_line_1 = clean_json_string_input(post_json, "root", "Address Line 1", post_errors)
    rqst_address_line_2 = clean_json_string_input(post_json, "root", "Address Line 2", post_errors, empty_string_allowed=True)
    if rqst_address_line_2 is None:
        rqst_address_line_2 = ''
    rqst_city = clean_json_string_input(post_json, "root", "City", post_errors)
    rqst_state = clean_json_string_input(post_json, "root", "State", post_errors)
    rqst_zipcode = clean_json_string_input(post_json, "root", "Zipcode", post_errors)
    rqst_country = clean_json_string_input(post_json, "root", "Country", post_errors)
    rqst_location_id = clean_json_int_input(post_json, "root", "Database ID", post_errors)

    if len(post_errors) == 0:
        address_instance, address_instance_created = Address.objects.get_or_create(address_line_1=rqst_address_line_1,
                                                                                   address_line_2=rqst_address_line_2,
                                                                                   city=rqst_city,
                                                                                   state_province=rqst_state,
                                                                                   zipcode=rqst_zipcode,
                                                                                   country=Country.objects.get(name=rqst_country))
        try:
            location_instance = NavMetricsLocation.objects.get(id=rqst_location_id)
            location_instance.name = rqst_location_name
            location_instance.address = address_instance
            location_instance.save()
            response_raw_data['Data'] = {"Database ID": location_instance.id}
        except NavMetricsLocation.DoesNotExist:
            post_errors.append('Nav Hub Location database entry does not exist for the name: {!s}'.format(str(rqst_location_name)))
        except NavMetricsLocation.MultipleObjectsReturned:
            post_errors.append('Multiple database entries exist for the name: {!s}'.format(str(rqst_location_name)))
        except IntegrityError:
            post_errors.append('Database entry already exists for the name: {!s}'.format(rqst_location_name))

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    return response_raw_data


def delete_nav_hub_location(response_raw_data, post_json, post_errors):
    rqst_location_id = clean_json_int_input(post_json, "root", "Database ID", post_errors)

    if len(post_errors) == 0:
        try:
            location_instance = NavMetricsLocation.objects.get(id=rqst_location_id)
            location_instance.delete()
            response_raw_data['Data'] = {"Database ID": "Deleted"}
        except NavMetricsLocation.DoesNotExist:
            post_errors.append('Location database entry does not exist for the id: {!s}'.format(str(rqst_location_id)))
        except NavMetricsLocation.MultipleObjectsReturned:
            post_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_location_id)))

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    return response_raw_data


def add_staff(response_raw_data, post_json, post_errors):
    rqst_usr_email = clean_json_string_input(post_json, "root", "Email", post_errors)
    rqst_usr_mpn = clean_json_string_input(post_json, "root", "MPN", post_errors, empty_string_allowed=True, none_allowed=True)
    if rqst_usr_mpn is None:
        rqst_usr_mpn = ''
    rqst_usr_f_name = clean_json_string_input(post_json, "root", "First Name", post_errors)
    rqst_usr_l_name = clean_json_string_input(post_json, "root", "Last Name", post_errors)
    rqst_county = clean_json_string_input(post_json, "root", "User County", post_errors)
    rqst_usr_type = clean_json_string_input(post_json, "root", "User Type", post_errors)
    rqst_base_locations = clean_list_input(post_json, "root", "Base Locations", post_errors, empty_list_allowed=True)
    rqst_base_locations = list(set(rqst_base_locations))
    base_location_objects = []
    location_errors = []
    if rqst_base_locations:
        for base_location_name in rqst_base_locations:
            try:
                base_location_object = NavMetricsLocation.objects.get(name=base_location_name)
                base_location_objects.append(base_location_object)
            except NavMetricsLocation.DoesNotExist:
                location_errors.append("No Nav Hub Location Database entry found for name: {!s}".format(base_location_name))

    if len(post_errors) == 0:
        usr_rqst_values = {"first_name": rqst_usr_f_name,
                           "last_name": rqst_usr_l_name,
                           "type": rqst_usr_type,
                           "county": rqst_county,
                           "mpn": rqst_usr_mpn}
        user_instance, user_instance_created = PICStaff.objects.get_or_create(email=rqst_usr_email,
                                                                              defaults=usr_rqst_values)
        if not user_instance_created:
            post_errors.append('Staff database entry already exists for the email: {!s}'.format(rqst_usr_email))
        else:
            user_instance.base_locations = base_location_objects
            user_instance.save()
            response_raw_data['Data'] = {"Database ID": user_instance.id}

    for location_error in location_errors:
        post_errors.append(location_error)
    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    return response_raw_data


def modify_staff(response_raw_data, post_json, post_errors):
    rqst_usr_id = clean_json_int_input(post_json, "root", "Database ID", post_errors)
    rqst_usr_email = clean_json_string_input(post_json, "root", "Email", post_errors)
    rqst_usr_mpn = clean_json_string_input(post_json, "root", "MPN", post_errors, empty_string_allowed=True, none_allowed=True)
    if rqst_usr_mpn is None:
        rqst_usr_mpn = ''
    rqst_usr_f_name = clean_json_string_input(post_json, "root", "First Name", post_errors)
    rqst_usr_l_name = clean_json_string_input(post_json, "root", "Last Name", post_errors)
    rqst_county = clean_json_string_input(post_json, "root", "User County", post_errors)
    rqst_usr_type = clean_json_string_input(post_json, "root", "User Type", post_errors)
    rqst_base_locations = clean_list_input(post_json, "root", "Base Locations", post_errors, empty_list_allowed=True)
    rqst_base_locations = list(set(rqst_base_locations))
    base_location_objects = []
    location_errors = []
    if rqst_base_locations:
        for base_location_name in rqst_base_locations:
            try:
                base_location_object = NavMetricsLocation.objects.get(name=base_location_name)
                base_location_objects.append(base_location_object)
            except NavMetricsLocation.DoesNotExist:
                location_errors.append("No Nav Hub Location Database entry found for name: {!s}".format(base_location_name))

    if len(post_errors) == 0:
        try:
            staff_instance = PICStaff.objects.get(id=rqst_usr_id)
            staff_instance.first_name = rqst_usr_f_name
            staff_instance.last_name = rqst_usr_l_name
            staff_instance.type = rqst_usr_type
            staff_instance.county = rqst_county
            staff_instance.email = rqst_usr_email
            staff_instance.mpn = rqst_usr_mpn
            staff_instance.base_locations = base_location_objects
            staff_instance.save()
            response_raw_data['Data'] = {"Database ID": staff_instance.id}
        except PICStaff.DoesNotExist:
            post_errors.append('Staff database entry does not exist for the id: {!s}'.format(str(rqst_usr_id)))
        except PICStaff.MultipleObjectsReturned:
            post_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_usr_id)))
        except IntegrityError:
            post_errors.append('Database entry already exists for the email: {!s}'.format(rqst_usr_email))

    for location_error in location_errors:
        post_errors.append(location_error)
    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    return response_raw_data


def delete_staff(response_raw_data, post_json, post_errors):
    rqst_usr_id = clean_json_int_input(post_json, "root", "Database ID", post_errors)

    if len(post_errors) == 0:
        try:
            staff_instance = PICStaff.objects.get(id=rqst_usr_id)
            staff_instance.delete()
            response_raw_data['Data'] = {"Database ID": "Deleted"}
        except PICStaff.DoesNotExist:
            post_errors.append('Staff database entry does not exist for the id: {!s}'.format(str(rqst_usr_id)))
        except PICStaff.MultipleObjectsReturned:
            post_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_usr_id)))

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    return response_raw_data


def add_consumer(response_raw_data, post_json, post_errors):
    rqst_consumer_email = clean_json_string_input(post_json, "root", "Email", post_errors, empty_string_allowed=True)
    rqst_consumer_f_name = clean_json_string_input(post_json, "root", "First Name", post_errors)
    rqst_consumer_m_name = clean_json_string_input(post_json, "root", "Middle Name", post_errors, empty_string_allowed=True)
    rqst_consumer_l_name = clean_json_string_input(post_json, "root", "Last Name", post_errors)
    rqst_consumer_plan = clean_json_string_input(post_json, "root", "Plan", post_errors, empty_string_allowed=True)
    rqst_consumer_met_nav_at = clean_json_string_input(post_json, "root", "Met Navigator At", post_errors)
    rqst_consumer_household_size = clean_json_int_input(post_json, "root", "Household Size", post_errors)
    rqst_consumer_phone = clean_json_string_input(post_json, "root", "Phone Number", post_errors, empty_string_allowed=True)
    rqst_consumer_pref_lang = clean_json_string_input(post_json, "root", "Preferred Language", post_errors, empty_string_allowed=True)
    rqst_navigator_notes = clean_list_input(post_json, "root", "Navigator Notes", post_errors, empty_list_allowed=True)
    rqst_nav_id = clean_json_int_input(post_json, "root", "Navigator Database ID", post_errors)

    rqst_address_line_1 = clean_json_string_input(post_json, "root", "Address Line 1", post_errors, empty_string_allowed=True)
    rqst_address_line_2 = clean_json_string_input(post_json, "root", "Address Line 2", post_errors, empty_string_allowed=True)
    if rqst_address_line_2 is None:
        rqst_address_line_2 = ''
    rqst_city = clean_json_string_input(post_json, "root", "City", post_errors, empty_string_allowed=True)
    rqst_state = clean_json_string_input(post_json, "root", "State", post_errors, empty_string_allowed=True)
    rqst_zipcode = clean_json_string_input(post_json, "root", "Zipcode", post_errors, empty_string_allowed=True)

    date_met_nav_dict = clean_dict_input(post_json, "root", "date_met_nav", post_errors, none_allowed=True)
    rqst_date_met_nav = None
    if date_met_nav_dict is not None:
        month = clean_json_int_input(date_met_nav_dict, "date_met_nav", "Month", post_errors)
        if month < 1 or month > 12:
            post_errors.append("Month must be between 1 and 12 inclusive")

        day = clean_json_int_input(date_met_nav_dict, "date_met_nav", "Day", post_errors)
        if day < 1 or day > 31:
            post_errors.append("Day must be between 1 and 31 inclusive")

        year = clean_json_int_input(date_met_nav_dict, "date_met_nav", "Year", post_errors)
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

        consumer_rqst_values = {"plan": rqst_consumer_plan,
                                "met_nav_at": rqst_consumer_met_nav_at,
                                "household_size": rqst_consumer_household_size,
                                "preferred_language": rqst_consumer_pref_lang}

        consumer_instance, consumer_instance_created = PICConsumer.objects.get_or_create(email=rqst_consumer_email,
                                                                                         first_name=rqst_consumer_f_name,
                                                                                         middle_name=rqst_consumer_m_name,
                                                                                         last_name=rqst_consumer_l_name,
                                                                                         address=address_instance,
                                                                                         phone=rqst_consumer_phone,
                                                                                         date_met_nav=rqst_date_met_nav,
                                                                                         defaults=consumer_rqst_values)
        if not consumer_instance_created:
            post_errors.append('Consumer database entry already exists for the email: {!s}'.format(rqst_consumer_email))
        else:
            try:
                nav_instance = PICStaff.objects.get(id=rqst_nav_id)
                consumer_instance.navigator = nav_instance
                consumer_instance.save()
            except PICStaff.DoesNotExist:
                post_errors.append('Staff database entry does not exist for the navigator id: {!s}'.format(str(rqst_nav_id)))

            if consumer_instance:
                old_consumer_notes = ConsumerNote.objects.filter(consumer=consumer_instance.id)
                for old_consumer_note in old_consumer_notes:
                    old_consumer_note.delete()

                for navigator_note in rqst_navigator_notes:
                    consumer_note_object = ConsumerNote(consumer=consumer_instance, navigator_notes=navigator_note)
                    consumer_note_object.save()
        response_raw_data['Data'] = {"Database ID": consumer_instance.id}

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    return response_raw_data


def modify_consumer(response_raw_data, post_json, post_errors):
    rqst_consumer_email = clean_json_string_input(post_json, "root", "Email", post_errors, empty_string_allowed=True)
    rqst_consumer_f_name = clean_json_string_input(post_json, "root", "First Name", post_errors)
    rqst_consumer_m_name = clean_json_string_input(post_json, "root", "Middle Name", post_errors, empty_string_allowed=True)
    rqst_consumer_l_name = clean_json_string_input(post_json, "root", "Last Name", post_errors)
    rqst_consumer_plan = clean_json_string_input(post_json, "root", "Plan", post_errors, empty_string_allowed=True)
    rqst_consumer_met_nav_at = clean_json_string_input(post_json, "root", "Met Navigator At", post_errors)
    rqst_consumer_household_size = clean_json_int_input(post_json, "root", "Household Size", post_errors)
    rqst_consumer_phone = clean_json_string_input(post_json, "root", "Phone Number", post_errors, empty_string_allowed=True)
    rqst_consumer_pref_lang = clean_json_string_input(post_json, "root", "Preferred Language", post_errors, empty_string_allowed=True)
    rqst_navigator_notes = clean_list_input(post_json, "root", "Navigator Notes", post_errors, empty_list_allowed=True)
    rqst_nav_id = clean_json_int_input(post_json, "root", "Navigator Database ID", post_errors)
    rqst_consumer_id = clean_json_int_input(post_json, "root", "Consumer Database ID", post_errors)

    rqst_address_line_1 = clean_json_string_input(post_json, "root", "Address Line 1", post_errors, empty_string_allowed=True)
    rqst_address_line_2 = clean_json_string_input(post_json, "root", "Address Line 2", post_errors, empty_string_allowed=True)
    if rqst_address_line_2 is None:
        rqst_address_line_2 = ''
    rqst_city = clean_json_string_input(post_json, "root", "City", post_errors, empty_string_allowed=True)
    rqst_state = clean_json_string_input(post_json, "root", "State", post_errors, empty_string_allowed=True)
    rqst_zipcode = clean_json_string_input(post_json, "root", "Zipcode", post_errors, empty_string_allowed=True)

    date_met_nav_dict = clean_dict_input(post_json, "root", "date_met_nav", post_errors, none_allowed=True)
    rqst_date_met_nav = None
    if date_met_nav_dict is not None:
        month = clean_json_int_input(date_met_nav_dict, "date_met_nav", "Month", post_errors)
        if month < 1 or month > 12:
            post_errors.append("Month must be between 1 and 12 inclusive")

        day = clean_json_int_input(date_met_nav_dict, "date_met_nav", "Day", post_errors)
        if day < 1 or day > 31:
            post_errors.append("Day must be between 1 and 31 inclusive")

        year = clean_json_int_input(date_met_nav_dict, "date_met_nav", "Year", post_errors)
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

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    return response_raw_data


def delete_consumer(response_raw_data, post_json, post_errors):
    rqst_consumer_id = clean_json_int_input(post_json, "root", "Consumer Database ID", post_errors)

    if len(post_errors) == 0:
        try:
            consumer_instance = PICConsumer.objects.get(id=rqst_consumer_id)
            consumer_instance.delete()
            response_raw_data['Data'] = {"Database ID": "Deleted"}
        except PICConsumer.DoesNotExist:
            post_errors.append('Consumer database entry does not exist for the id: {!s}'.format(str(rqst_consumer_id)))
        except PICConsumer.MultipleObjectsReturned:
            post_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_consumer_id)))

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    return response_raw_data


def add_or_update_metrics_entity(response_raw_data, post_json, post_errors):
    rqst_usr_email = clean_json_string_input(post_json, "root", "Email", post_errors)

    consumer_metrics = clean_dict_input(post_json, "root", "Consumer Metrics", post_errors)
    if consumer_metrics is not None:
        consumer_metrics = post_json["Consumer Metrics"]

        rqst_no_general_assis = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_general_assis",
                                                 post_errors)
        rqst_no_plan_usage_assis = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_plan_usage_assis",
                                                 post_errors)
        rqst_no_locating_provider_assis = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_locating_provider_assis",
                                                 post_errors)
        rqst_no_billing_assis = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_billing_assis",
                                                 post_errors)
        rqst_no_enroll_apps_started = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_enroll_apps_started",
                                                 post_errors)
        rqst_no_enroll_qhp = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_enroll_qhp",
                                                 post_errors)
        rqst_no_enroll_abe_chip = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_enroll_abe_chip",
                                                 post_errors)
        rqst_no_enroll_shop = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_enroll_shop",
                                                 post_errors)
        rqst_no_referrals_agents_brokers = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_referrals_agents_brokers",
                                                 post_errors)
        rqst_no_referrals_ship_medicare = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_referrals_ship_medicare",
                                                 post_errors)
        rqst_no_referrals_other_assis_programs = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_referrals_other_assis_programs",
                                                 post_errors)
        rqst_no_referrals_issuers = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_referrals_issuers",
                                                 post_errors)
        rqst_no_referrals_doi = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_referrals_doi",
                                                 post_errors)
        rqst_no_mplace_tax_form_assis = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_mplace_tax_form_assis",
                                                 post_errors)
        rqst_no_mplace_exempt_assis = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_mplace_exempt_assis",
                                                 post_errors)
        rqst_no_qhp_abe_appeals = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_qhp_abe_appeals",
                                                 post_errors)
        rqst_no_data_matching_mplace_issues = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_data_matching_mplace_issues",
                                                 post_errors)
        rqst_no_sep_eligible = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_sep_eligible",
                                                 post_errors)
        rqst_no_employ_spons_cov_issues = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_employ_spons_cov_issues",
                                                 post_errors)
        rqst_no_aptc_csr_assis = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_aptc_csr_assis",
                                                 post_errors)
        rqst_cmplx_cases_mplace_issues = clean_json_string_input(consumer_metrics, "Consumer Metrics", "cmplx_cases_mplace_issues", post_errors,
                                                   empty_string_allowed=True)

        rqst_metrics_county = clean_json_string_input(consumer_metrics, "Consumer Metrics", "County", post_errors)
        rqst_metrics_location = clean_json_string_input(consumer_metrics, "Consumer Metrics", "Location", post_errors)

        metrics_date_dict = clean_dict_input(consumer_metrics, "Consumer Metrics", "Metrics Date", post_errors)
        if metrics_date_dict is not None:
            month = clean_json_int_input(metrics_date_dict, "Metrics Date", "Month", post_errors)
            if month < 1 or month > 12:
                post_errors.append("Month must be between 1 and 12 inclusive")

            day = clean_json_int_input(metrics_date_dict, "Metrics Date", "Day", post_errors)
            if day < 1 or day > 31:
                post_errors.append("Day must be between 1 and 31 inclusive")

            year = clean_json_int_input(metrics_date_dict, "Metrics Date", "Year", post_errors)
            if year < 1 or year > 9999:
                post_errors.append("Year must be between 1 and 9999 inclusive")

            if len(post_errors) == 0:
                metrics_date = datetime.date(year, month, day)

    # if there are no parsing errors, get or create database entries for consumer, location, and point of contact
    # create and save database entry for appointment
    if len(post_errors) == 0:
        # usr_rqst_values = {"first_name": rqst_usr_f_name,
        #                    "last_name": rqst_usr_l_name,
        #                    "type": rqst_usr_type,}
        # user_instance, user_instance_created = PICStaff.objects.get_or_create(email=rqst_usr_email,
        #                                                                       defaults=usr_rqst_values)
        try:
            metrics_instance_message = 'Metrics Entry Updated'
            user_instance = PICStaff.objects.get(email__iexact=rqst_usr_email)

            try:
                metrics_instance = MetricsSubmission.objects.get(staff_member=user_instance, submission_date=metrics_date)
            except models.ObjectDoesNotExist:
                metrics_instance = MetricsSubmission(staff_member=user_instance, submission_date=metrics_date)
                metrics_instance_message = 'Metrics Entry Created'
            except MetricsSubmission.MultipleObjectsReturned:
                post_errors.append("Multiple metrics entries exist for this date")

                response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
                response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
                return response

            metrics_instance.no_general_assis = rqst_no_general_assis
            metrics_instance.no_plan_usage_assis = rqst_no_plan_usage_assis
            metrics_instance.no_locating_provider_assis = rqst_no_locating_provider_assis
            metrics_instance.no_billing_assis = rqst_no_billing_assis
            metrics_instance.no_enroll_apps_started = rqst_no_enroll_apps_started
            metrics_instance.no_enroll_qhp = rqst_no_enroll_qhp
            metrics_instance.no_enroll_abe_chip = rqst_no_enroll_abe_chip
            metrics_instance.no_enroll_shop = rqst_no_enroll_shop
            metrics_instance.no_referrals_agents_brokers = rqst_no_referrals_agents_brokers
            metrics_instance.no_referrals_ship_medicare = rqst_no_referrals_ship_medicare
            metrics_instance.no_referrals_other_assis_programs = rqst_no_referrals_other_assis_programs
            metrics_instance.no_referrals_issuers = rqst_no_referrals_issuers
            metrics_instance.no_referrals_doi = rqst_no_referrals_doi
            metrics_instance.no_mplace_tax_form_assis = rqst_no_mplace_tax_form_assis
            metrics_instance.no_mplace_exempt_assis = rqst_no_mplace_exempt_assis
            metrics_instance.no_qhp_abe_appeals = rqst_no_qhp_abe_appeals
            metrics_instance.no_data_matching_mplace_issues = rqst_no_data_matching_mplace_issues
            metrics_instance.no_sep_eligible = rqst_no_sep_eligible
            metrics_instance.no_employ_spons_cov_issues = rqst_no_employ_spons_cov_issues
            metrics_instance.no_aptc_csr_assis = rqst_no_aptc_csr_assis
            metrics_instance.cmplx_cases_mplace_issues = rqst_cmplx_cases_mplace_issues
            metrics_instance.county = rqst_metrics_county

            try:
                location_instance = NavMetricsLocation.objects.get(name=rqst_metrics_location)
                metrics_instance.location = location_instance
                metrics_instance.zipcode = location_instance.address.zipcode
            except models.ObjectDoesNotExist:
                post_errors.append("Location instance does not exist for given location name: {!s}.".format(rqst_metrics_location))
            except MetricsSubmission.MultipleObjectsReturned:
                post_errors.append("Multiple location instances exist for given location name: {!s}".format(rqst_metrics_location))

            if len(post_errors) == 0:
                response_raw_data["Status"]["Message"] = [metrics_instance_message]
                metrics_instance.save()

                rqst_plan_stats = clean_list_input(consumer_metrics, "Consumer Metrics", "Plan Stats", post_errors)
                metrics_instance_plan_stats = PlanStat.objects.filter(metrics_submission=metrics_instance.id)
                for instance_plan_stat in metrics_instance_plan_stats:
                    instance_plan_stat.delete()
                if rqst_plan_stats is not None:
                    for rqst_plan_stat_dict in rqst_plan_stats:
                        planstatobject = PlanStat()
                        planstatobject.plan_name = clean_json_string_input(rqst_plan_stat_dict, "Plans Dict", "Issuer Name", post_errors)
                        planstatobject.premium_type = clean_json_string_input(rqst_plan_stat_dict, "Plans Dict", "Premium Type", post_errors)
                        planstatobject.metal_level = clean_json_string_input(rqst_plan_stat_dict, "Plans Dict", "Metal Level", post_errors)
                        planstatobject.enrollments = clean_json_int_input(rqst_plan_stat_dict, "Plans Dict", "Enrollments", post_errors)

                        plan_name_valid = planstatobject.check_plan_choices()
                        premium_type_valid = planstatobject.check_premium_choices()
                        metal_level_valid = planstatobject.check_metal_choices()
                        if not plan_name_valid:
                            post_errors.append("Plan: {!s} is not part of member plans".format(planstatobject.plan_name))
                        if not premium_type_valid:
                            post_errors.append("Premium Type: {!s} is not a valid premium type".format(planstatobject.premium_type))
                        if not metal_level_valid:
                            post_errors.append("Metal: {!s} is not a valid metal level".format(planstatobject.metal_level))

                        if plan_name_valid and premium_type_valid and metal_level_valid:
                            planstatobject.metrics_submission = metrics_instance
                            planstatobject.save()
                    # for plan, enrollments in rqst_plan_stats.items():
                    #     planstatobject = PlanStat()
                    #     planstatobject.plan_name = plan
                    #     if planstatobject.check_plan_choices():
                    #         rqst_plan_enrollments = clean_json_int_input(rqst_plan_stats, "Plan Stats", plan, post_errors)
                    #         if rqst_plan_enrollments is not None:
                    #             planstatobject.enrollments = rqst_plan_enrollments
                    #             planstatobject.save()
                    #             metrics_instance.plan_stats.add(planstatobject)
                    #     else:
                    #         post_errors.append("Plan: {!s} is not part of member plans".format(plan))

        except models.ObjectDoesNotExist:
            post_errors.append("Staff database entry does not exist for email: {!s}".format(rqst_usr_email))

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    return response_raw_data


def check_or_create_navigator_google_cal(credential):
    service = build_authorized_cal_http_service_object(credential)

    navigator_calendar_found, _ = check_cal_objects_for_nav_cal(service)

    if not navigator_calendar_found:
        service = build_authorized_cal_http_service_object(credential)
        cal_id = add_nav_cal_to_google_cals(service)


def check_cal_objects_for_nav_cal(service):
    cal_list_entry_objects = service.calendarList().list(showHidden=True).execute()["items"]

    navigator_calendar_found = False
    navigator_calendar_id = None
    for cal_list_entry in cal_list_entry_objects:
        calendar_title = cal_list_entry["summary"]
        if calendar_title == "Navigator-Consumer Appointments (DO NOT CHANGE)":
            navigator_calendar_found = True
            navigator_calendar_id = cal_list_entry["id"]
            break

    return navigator_calendar_found, navigator_calendar_id


def add_nav_cal_to_google_cals(service):
    insert_args = {"summary": "Navigator-Consumer Appointments (DO NOT CHANGE)",
                   "description": "DO NOT CHANGE THE TITLE OF THIS CALENDAR. IF YOU DO, YOU WILL NOT RECIEVE NEW CONSUMER APPOINTMENTS."}
    new_cal = service.calendars().insert(body=insert_args).execute()

    return new_cal["id"]


def build_authorized_cal_http_service_object(credential):
    http = httplib2.Http()
    http = credential.authorize(http)
    service = build("calendar", "v3", http=http)

    return service


def add_nav_apt_to_google_calendar(post_json, post_errors):
    scheduled_appointment = {}
    rqst_nav_id = clean_json_int_input(post_json, "root", "Navigator ID", post_errors)
    rqst_apt_datetime = clean_json_string_input(post_json, "root", "Appointment Date and Time", post_errors)
    if not isinstance(rqst_apt_datetime, str):
        post_errors.append("{!s} is not a string, Preferred Times must be a string iso formatted date and time".format(str(rqst_apt_datetime)))

    consumer_info = get_or_create_consumer_instance(rqst_nav_id, post_json, post_errors)
    try:
        picstaff_object = PICStaff.objects.get(id=rqst_nav_id)
        credentials_object = CredentialsModel.objects.get(id=picstaff_object)
        nav_info = picstaff_object.return_values_dict()
        if credentials_object.credential.invalid:
            credentials_object.delete()
            post_errors.append('Google Credentials database entry is invalid for the navigator with id: {!s}'.format(str(rqst_nav_id)))
        else:
            scheduled_appointment = send_add_apt_rqst_to_google(credentials_object.credential, rqst_apt_datetime, consumer_info, nav_info, post_errors)

    except PICStaff.DoesNotExist:
        post_errors.append('Navigator database entry does not exist for the id: {!s}'.format(str(rqst_nav_id)))
    except CredentialsModel.DoesNotExist:
        post_errors.append('Google Credentials database entry does not exist for the navigator with id: {!s}'.format(str(rqst_nav_id)))

    return scheduled_appointment, consumer_info["Database ID"]


def get_or_create_consumer_instance(rqst_nav_id, post_json, post_errors):
    consumer_info = {}
    rqst_consumer_info = clean_dict_input(post_json, "root", "Consumer Info", post_errors)

    if not post_errors and rqst_consumer_info:
        rqst_consumer_email = clean_json_string_input(rqst_consumer_info, "Consumer Info", "Email", post_errors, empty_string_allowed=True)
        rqst_consumer_f_name = clean_json_string_input(rqst_consumer_info, "Consumer Info", "First Name", post_errors)
        rqst_consumer_m_name = clean_json_string_input(rqst_consumer_info, "Consumer Info", "Middle Name", post_errors, empty_string_allowed=True)
        rqst_consumer_l_name = clean_json_string_input(rqst_consumer_info, "Consumer Info", "Last Name", post_errors)
        rqst_consumer_plan = clean_json_string_input(rqst_consumer_info, "Consumer Info", "Plan", post_errors, empty_string_allowed=True)
        rqst_consumer_met_nav_at = "Patient Assist"
        rqst_consumer_household_size = clean_json_int_input(rqst_consumer_info, "Consumer Info", "Household Size", post_errors)
        rqst_consumer_phone = clean_json_string_input(rqst_consumer_info, "Consumer Info", "Phone Number", post_errors)
        rqst_consumer_pref_lang = clean_json_string_input(rqst_consumer_info, "Consumer Info", "Preferred Language", post_errors, empty_string_allowed=True)

        rqst_address_line_1 = clean_json_string_input(rqst_consumer_info, "Consumer Info", "Address Line 1", post_errors, empty_string_allowed=True)
        rqst_address_line_2 = clean_json_string_input(rqst_consumer_info, "Consumer Info", "Address Line 2", post_errors, empty_string_allowed=True)
        if rqst_address_line_2 is None:
            rqst_address_line_2 = ''
        rqst_city = clean_json_string_input(rqst_consumer_info, "Consumer Info", "City", post_errors, empty_string_allowed=True)
        rqst_state = clean_json_string_input(rqst_consumer_info, "Consumer Info", "State", post_errors, empty_string_allowed=True)
        rqst_zipcode = clean_json_string_input(rqst_consumer_info, "Consumer Info", "Zipcode", post_errors, empty_string_allowed=True)
        rqst_date_met_nav = datetime.datetime.utcnow()

        if len(post_errors) == 0:
            address_instance = None
            if rqst_address_line_1 != '' and rqst_city != '' and rqst_state != '' and rqst_zipcode != '':
                address_instance, address_instance_created = Address.objects.get_or_create(address_line_1=rqst_address_line_1,
                                                                                           address_line_2=rqst_address_line_2,
                                                                                           city=rqst_city,
                                                                                           state_province=rqst_state,
                                                                                           zipcode=rqst_zipcode,
                                                                                           country=Country.objects.all()[0])

            consumer_rqst_values = {"plan": rqst_consumer_plan,
                                    "met_nav_at": rqst_consumer_met_nav_at,
                                    "household_size": rqst_consumer_household_size,
                                    "preferred_language": rqst_consumer_pref_lang}

            consumer_instance, consumer_instance_created = PICConsumer.objects.get_or_create(email=rqst_consumer_email,
                                                                                             first_name=rqst_consumer_f_name,
                                                                                             middle_name=rqst_consumer_m_name,
                                                                                             last_name=rqst_consumer_l_name,
                                                                                             address=address_instance,
                                                                                             phone=rqst_consumer_phone,
                                                                                             date_met_nav=rqst_date_met_nav,
                                                                                             defaults=consumer_rqst_values)

            try:
                nav_instance = PICStaff.objects.get(id=rqst_nav_id)
                consumer_instance.navigator = nav_instance
                consumer_instance.save()
            except PICStaff.DoesNotExist:
                post_errors.append('Staff database entry does not exist for the navigator id: {!s}'.format(str(rqst_nav_id)))

            consumer_info = consumer_instance.return_values_dict()

    return consumer_info


def send_add_apt_rqst_to_google(credential, rqst_apt_datetime, consumer_info, nav_info, post_errors):
    scheduled_appointment = {}
    if not post_errors:
        try:
            apt_end_timestamp = dateutil.parser.parse(rqst_apt_datetime) + datetime.timedelta(minutes=30)
            service = build_authorized_cal_http_service_object(credential)

            navigator_calendar_found, navigator_calendar_id = check_cal_objects_for_nav_cal(service)
            if not navigator_calendar_found:
                post_errors.append("Navigator calendar not found for this navigator, creating it...")
                navigator_calendar_id = add_nav_cal_to_google_cals(service)

            service = build_authorized_cal_http_service_object(credential)
            nav_apt_args = {"summary": "Navigator ({!s} {!s}) appointment with {!s} {!s}".format(nav_info["First Name"],
                                                                                                 nav_info["Last Name"],
                                                                                                 consumer_info["First Name"],
                                                                                                 consumer_info["Last Name"]),
                            "description": "Consumer will be expecting a call at {!s}\nOther Consumer Info:\nFirst Name: {!s}\nLast Name: {!s}\nEmail: {!s}".format(consumer_info["Phone Number"],
                                                                                                                                                                    consumer_info["First Name"],
                                                                                                                                                                    consumer_info["Last Name"],
                                                                                                                                                                    consumer_info["Email"]),
                            "start": {"dateTime": rqst_apt_datetime + 'Z'},
                            "end": {"dateTime": apt_end_timestamp.isoformat() + 'Z'}
                            }
            navigator_appointment_object = service.events().insert(calendarId=navigator_calendar_id, body=nav_apt_args, sendNotifications=True).execute()

            scheduled_appointment["Navigator Name"] = "{!s} {!s}".format(nav_info["First Name"],nav_info["Last Name"])
            scheduled_appointment["Navigator Database ID"] = nav_info["Database ID"]
            scheduled_appointment["Appointment Date and Time"] = rqst_apt_datetime
            scheduled_appointment["Appointment Title"] = navigator_appointment_object["summary"]
            scheduled_appointment["Appointment Summary"] = navigator_appointment_object["description"]

        except ValueError:
            post_errors.append("{!s} is not a properly iso formatted date and time, Preferred Times must be a string iso formatted date and time".format(rqst_apt_datetime))

    return scheduled_appointment


def delete_nav_apt_from_google_calendar(post_json, post_errors):
    pass
