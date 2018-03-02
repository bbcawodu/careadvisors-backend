"""
Defines views that are mapped to url configurations
"""
from django.http import HttpResponse
from django.shortcuts import render
from picmodels.models import PICConsumer, PICStaff
from presencescheduler.models import Appointment, Location
import datetime, json, sys, re
from django.views.decorators.csrf import csrf_exempt


def clean_json_string_input(json_dict, dict_name, dict_key, post_errors, empty_string_allowed=False,
                            none_allowed=False):
    if dict_key not in json_dict:
        post_errors.append("{!r} key not found in {!r} dictionary".format(dict_key, dict_name))
    elif json_dict[dict_key] == "" and empty_string_allowed is False:
        post_errors.append("Value for {!r} in {!r} dictionary is an empty string".format(dict_key, dict_name))
    elif json_dict[dict_key] is None and none_allowed is False:
        post_errors.append("Value for {!r} in {!r} dictionary is Null".format(dict_key, dict_name))
    else:
        return str(json_dict[dict_key])
    return None


def clean_json_int_input(json_dict, dict_name, dict_key, post_errors):
    if dict_key not in json_dict:
        post_errors.append("{!r} key not found in {!r} dictionary".format(dict_key, dict_name))
    elif json_dict[dict_key] is None:
        post_errors.append("Value for {!r} in {!r} dictionary is Null".format(dict_key, dict_name))
    else:
        return int(json_dict[dict_key])
    return None


def clean_dict_input(json_dict, dict_name, dict_key, post_errors):
    if dict_key not in json_dict:
        post_errors.append("{!r} key not found in {!r} dictionary".format(dict_key, dict_name))
    elif json_dict[dict_key] is None:
        post_errors.append("Value for {!r} in {!r} dictionary is Null".format(dict_key, dict_name))
    elif not isinstance(json_dict[dict_key], dict):
        post_errors.append("Value for {!r} in {!r} dictionary is not a dictionary".format(dict_key, dict_name))
    elif json_dict[dict_key] == {}:
        post_errors.append("Value for {!r} in {!r} dictionary is an empty dictionary".format(dict_key, dict_name))
    else:
        return json_dict[dict_key]
    return None


# defines view for saving scheduled appointments to the database
@csrf_exempt
def appointment_submission_handler(request):
    # initialize dictionary for response data, including parsing errors
    response_raw_data = {'status': {"Error Code": 0, "Version": 1.0}}
    post_errors = []

    if request.method == 'POST' or request.is_ajax():
        post_data = request.body
        post_json = json.loads(post_data)

        response_raw_data["Appointment Instance"] = {}
        request_consumer_email = clean_json_string_input(post_json, "root", "Email", post_errors)
        request_consumer_first_name = clean_json_string_input(post_json, "root", "First Name", post_errors)
        request_consumer_last_name = clean_json_string_input(post_json, "root", "Last Name", post_errors)
        request_consumer_phone = clean_json_string_input(post_json, "root", "Phone Number", post_errors)
        request_consumer_preferred_language = clean_json_string_input(post_json, "root", "Preferred Language",
                                                                      post_errors, empty_string_allowed=True)
        request_consumer_best_contact_time = clean_json_string_input(post_json, "root", "Best Contact Time",
                                                                     post_errors, empty_string_allowed=True)

        appointment_information = clean_dict_input(post_json, "root", "Appointment", post_errors)
        if appointment_information is not None:
            request_location_name = clean_json_string_input(appointment_information, "Appointment Information", "Name",
                                                            post_errors)
            request_appointment_street_address = clean_json_string_input(appointment_information,
                                                                         "Appointment Information","Street Address",
                                                                         post_errors)
            request_appointment_city = clean_json_string_input(appointment_information, "Appointment Information",
                                                               "City", post_errors)
            request_appointment_state = clean_json_string_input(appointment_information, "Appointment Information",
                                                                "State", post_errors)
            request_appointment_zip = clean_json_string_input(appointment_information, "Appointment Information",
                                                              "Zip Code", post_errors)
            if len(post_errors) == 0:
                request_appointment_address = "{!s}, {!s} {!s}, {!s}".format(request_appointment_street_address,
                                                                             request_appointment_city,
                                                                             request_appointment_state,
                                                                             request_appointment_zip)
            request_appointment_location_phone = clean_json_string_input(appointment_information,
                                                                         "Appointment Information", "Phone Number",
                                                                         post_errors)

            appointment_slot_info = clean_dict_input(appointment_information, "Appointment Information",
                                                     "Appointment Slot", post_errors)
            if appointment_slot_info is not None:
                date_dictionary = clean_dict_input(appointment_slot_info, "Appointment Slot", "Date", post_errors)
                if date_dictionary is not None:
                    month = clean_json_int_input(date_dictionary, "Date", "Month", post_errors)
                    if month < 1 or month > 12:
                        post_errors.append("Month must be between 1 and 12 inclusive")

                    day = clean_json_int_input(date_dictionary, "Date", "Day", post_errors)
                    if day < 1 or day > 31:
                        post_errors.append("Day must be between 1 and 31 inclusive")

                    year = clean_json_int_input(date_dictionary, "Date", "Year", post_errors)
                    if year < 1 or year > 9999:
                        post_errors.append("Year must be between 1 and 9999 inclusive")

                    if len(post_errors) == 0:
                        apt_date = datetime.date(year, month, day).isoformat()
                        request_appointment_date = str(apt_date)

                start_dictionary = clean_dict_input(appointment_slot_info, "Appointment Slot", "Start Time",
                                                    post_errors)
                if start_dictionary is not None:
                    hour = clean_json_int_input(start_dictionary, "Start Time", "Hour", post_errors)
                    if hour not in range(24):
                        post_errors.append("Hour must be between 0 and 23 inclusive")

                    minutes = clean_json_int_input(start_dictionary, "Start Time", "Minutes", post_errors)
                    if minutes not in range(60):
                        post_errors.append("Minute must be between 0 and 59 inclusive")

                    if len(post_errors) == 0:
                        request_appointment_start_time = str(datetime.time(hour=hour, minute=minutes).isoformat())

                end_dictionary = clean_dict_input(appointment_slot_info, "Appointment Slot", "End Time", post_errors)
                if end_dictionary is not None:
                    hour = clean_json_int_input(end_dictionary, "End Time", "Hour", post_errors)
                    if hour not in range(24):
                        post_errors.append("Hour must be between 0 and 23 inclusive")

                    minutes = clean_json_int_input(end_dictionary, "End Time", "Minutes", post_errors)
                    if minutes not in range(60):
                        post_errors.append("Minute must be between 0 and 59 inclusive")

                    if len(post_errors) == 0:
                        request_appointment_end_time = str(datetime.time(hour=hour, minute=minutes).isoformat())

            appointment_poc_info = clean_dict_input(appointment_information, "Appointment Information",
                                                    "Point of Contact", post_errors)
            if appointment_poc_info is not None:
                request_poc_first_name = clean_json_string_input(appointment_poc_info, "Point of Contact", "First Name",
                                                                 post_errors)
                request_poc_last_name = clean_json_string_input(appointment_poc_info, "Point of Contact", "Last Name",
                                                                post_errors)
                request_poc_email = clean_json_string_input(appointment_poc_info, "Point of Contact", "Email",
                                                            post_errors)
                request_poc_type = clean_json_string_input(appointment_poc_info, "Point of Contact", "Type",
                                                           post_errors)

        # if there are no parsing errors, get or create database entries for consumer, location, and point of contact
        # create and save database entry for appointment
        if len(post_errors) == 0:
            consumer_request_values = {"first_name": request_consumer_first_name,
                                       "last_name": request_consumer_last_name,
                                       "phone": request_consumer_phone,
                                       "preferred_language": request_consumer_preferred_language,
                                       "best_contact_time": request_consumer_best_contact_time}
            pic_consumer, pic_consumer_created = PICConsumer.objects.get_or_create(email=request_consumer_email,
                                                                                   defaults=consumer_request_values)

            location_request_values = {"address": request_appointment_address,
                                       "phone": request_appointment_location_phone}
            appointment_location, appointment_location_created = Location.objects.get_or_create(name=request_location_name,
                                                                                                defaults=location_request_values)

            poc_request_values = {"first_name": request_poc_first_name,
                                  "last_name": request_poc_last_name,
                                  "type": request_poc_type}
            appointment_poc, appointment_poc_created = PICStaff.objects.get_or_create(email=request_poc_email,
                                                                                      defaults=poc_request_values)
            new_appointment = Appointment(consumer=pic_consumer,
                                          location=appointment_location,
                                          poc=appointment_poc,
                                          date=request_appointment_date,
                                          start_time=request_appointment_start_time,
                                          end_time=request_appointment_end_time)
            new_appointment.save()

            response_raw_data["consumer info"] = consumer_request_values
            response_raw_data["location"] = location_request_values
            response_raw_data["poc info"] = poc_request_values

        # add parsing errors to response dictionary
        else:
            response_raw_data["status"]["Error Code"] = 1
            response_raw_data["status"]["Errors"] = post_errors

            error_message = ""
            for message in post_errors:
                error_message = error_message + message + ", "
            print(error_message)
            sys.stdout.flush()

    # if a GET request is made, add error message to response data
    else:
        response_raw_data["status"]["Error Code"] = 1
        post_errors.append("Request needs POST data")
        response_raw_data["status"]["Errors"] = post_errors
        for message in post_errors:
            print(message)
        sys.stdout.flush()

    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response


# defines view for member list display page
def appointment_viewing_handler(request):
    all_appointments = Appointment.objects.all()
    return render(request, 'appointment_list.html', {'appointment_list': all_appointments})

