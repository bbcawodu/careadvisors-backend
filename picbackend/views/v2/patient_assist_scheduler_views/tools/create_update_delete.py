"""
Defines utility functions and classes for views that use the the Google API
- Need to update exception catching for google API email calls to make them more specific
"""

import datetime

import dateutil.parser
import httplib2
import mandrill
import pytz
from bdateutil import isbday
from dateutil.tz import tzutc
from django import forms
from django.core.validators import validate_email
from googleapiclient.discovery import build
from googleapiclient.http import BatchHttpRequest
from pandas import bdate_range
from pandas.tseries.offsets import BDay
from random import shuffle

from picbackend.views.utils import clean_dict_value_from_dict_object
from picbackend.views.utils import clean_int_value_from_dict_object
from picbackend.views.utils import clean_string_value_from_dict_object

from picbackend.views.v2.consumer_views.tools.create_update_delete import validate_put_rqst_params
from picmodels.models import CredentialsModel
from picmodels.models import PICStaff
from picmodels.models import PICConsumer

START_OF_BUSINESS_TIMESTAMP = datetime.time(hour=15, minute=0, second=0, microsecond=0)
END_OF_BUSINESS_TIMESTAMP = datetime.time(hour=23, minute=0, second=0, microsecond=0)


def check_or_create_navigator_google_cal(credential, err_msg_list):
    """
    This function checks a navigator's list of google calendars for the 'Navigator-Consumer Appointments (DO NOT CHANGE)'
    calendar. If it's not present, it adds it.

    :param credential: (type: CredentialsField) Google OAuth2 Credentials object
    :param err_msg_list: (type: list) list of error messages
    :return: None
    """

    service = build_authorized_cal_http_service_object(credential)

    navigator_calendar_found, _ = check_cal_objects_for_nav_cal(service, err_msg_list)

    if not navigator_calendar_found:
        service = build_authorized_cal_http_service_object(credential)
        _ = add_nav_cal_to_google_cals(service, err_msg_list)


def check_cal_objects_for_nav_cal(service, err_msg_list):
    """
    This function checks a navigator's list of google calendars for the 'Navigator-Consumer Appointments (DO NOT CHANGE)'
    calendar. Returns True if calendar is found and False otherwise. Returns calendar id if calendar is found.

    :param service: (type: service object) Authenticated Google Calendar API service object
    :param err_msg_list: (type: list) list of error messages
    :return:
    """

    navigator_calendar_found = False
    navigator_calendar_id = None

    try:
        cal_list_entry_objects = service.calendarList().list(showHidden=True).execute()["items"]

        for cal_list_entry in cal_list_entry_objects:
            calendar_title = cal_list_entry["summary"]
            if calendar_title == "Navigator-Consumer Appointments (DO NOT CHANGE)":
                navigator_calendar_found = True
                navigator_calendar_id = cal_list_entry["id"]
                break
    except Exception:
        err_msg_list.append("Call to Google failed, Check API call")

    return navigator_calendar_found, navigator_calendar_id


def add_nav_cal_to_google_cals(service, err_msg_list):
    """
    This function adds the 'Navigator-Consumer Appointments (DO NOT CHANGE)' calendar to the list of a given navigator's
    google calendars.

    :param service: (type: service object) Authenticated Google Calendar API service object
    :param err_msg_list: (type: list) list of error messages
    :return:
    """

    cal_id = None
    try:
        insert_args = {"summary": "Navigator-Consumer Appointments (DO NOT CHANGE)",
                       "description": "DO NOT CHANGE THE TITLE OF THIS CALENDAR. IF YOU DO, YOU WILL NOT RECIEVE NEW CONSUMER APPOINTMENTS."}
        new_cal = service.calendars().insert(body=insert_args).execute()
        cal_id = new_cal["id"]
    except Exception:
        err_msg_list.append("Call to Google failed, Check API call")

    return cal_id


def build_authorized_cal_http_service_object(credential):
    """
    This function takes a valid credentials object and returns a service object which can be used to make requests
    to the Google Calendar API

    :param credential: (type: CredentialsField) Google OAuth2 Credentials object
    :return:
    """

    http = httplib2.Http()
    http = credential.authorize(http)
    service = build("calendar", "v3", http=http)

    return service


def add_nav_apt_to_google_calendar(post_data, post_errors):
    """
    This function takes a dictionary populated with data about a consumer appointment with a navigator, adds it to the
    navigator's 'Navigator-Consumer Appointments (DO NOT CHANGE)' calendar, and sends an email notification to the
    consumer

    :param post_data: (type: dictionary) dictionary with Patient Assist appointment info
    :param post_errors: (type: list) list of error messages
    :return:
    """

    scheduled_appointment = {}
    rqst_nav_id = clean_int_value_from_dict_object(post_data, "root", "navigator_id", post_errors)
    rqst_apt_datetime = clean_string_value_from_dict_object(post_data, "root", "Appointment Date and Time", post_errors)
    if not isinstance(rqst_apt_datetime, str):
        post_errors.append("{!s} is not a string, Preferred Times must be a string iso formatted date and time".format(str(rqst_apt_datetime)))

    consumer_info = create_consumer_instance_from_apt_rqst(rqst_nav_id, post_data, post_errors)

    if not post_errors:
        try:
            picstaff_object = PICStaff.objects.get(id=rqst_nav_id)
            credentials_object = CredentialsModel.objects.get(id=picstaff_object)
            nav_info = picstaff_object.return_values_dict()
            if credentials_object.credential.invalid:
                credentials_object.delete()
                post_errors.append('Google Credentials database entry is invalid for the navigator with id: {!s}'.format(str(rqst_nav_id)))
            else:
                scheduled_appointment = send_add_apt_rqst_to_google_and_email_consumer(credentials_object.credential, rqst_apt_datetime, consumer_info, nav_info, post_errors)

        except PICStaff.DoesNotExist:
            post_errors.append('Navigator database entry does not exist for the id: {!s}'.format(str(rqst_nav_id)))
        except CredentialsModel.DoesNotExist:
            post_errors.append('Google Credentials database entry does not exist for the navigator with id: {!s}'.format(str(rqst_nav_id)))

    return scheduled_appointment, consumer_info


def create_consumer_instance_from_apt_rqst(rqst_nav_id, post_data, post_errors):
    """
    This function takes a dictionary populated with data about a consumer appointment with a navigator and creates a new
    PICConsumer database instance from that data

    :param rqst_nav_id:
    :param post_data: (type: dictionary) dictionary with PIC consumer info
    :param post_errors: (type: list) list of error messages
    :return:
    """

    consumer_info = {}
    rqst_consumer_info = clean_dict_value_from_dict_object(post_data, "root", "Consumer Info", post_errors)

    if not post_errors and rqst_consumer_info:
        rqst_consumer_info['db_action'] = "create"
        now_date_time = datetime.datetime.utcnow()
        rqst_consumer_info['date_met_nav'] = {"Day": now_date_time.day, "Month": now_date_time.month, "Year": now_date_time.year}
        rqst_consumer_info["met_nav_at"] = "Patient Assist"
        rqst_consumer_info["consumer_notes"] = []
        rqst_consumer_info['force_create_consumer'] = True
        rqst_consumer_info["navigator_id"] = rqst_nav_id

        new_consumer_params = validate_put_rqst_params(rqst_consumer_info, post_errors)
        matching_consumer_instances, consumer_instance, backup_consumer_obj = PICConsumer.create_row_w_validated_params(
            new_consumer_params,
            post_errors
        )

        if not post_errors:
            consumer_info = consumer_instance.return_values_dict()

    return consumer_info


def send_add_apt_rqst_to_google_and_email_consumer(credential, rqst_apt_datetime, consumer_info, nav_info, post_errors):
    """
    This function takes a dictionary populated with data about a consumer appointment with a navigator, adds the appointment
    to the navigators 'Navigator-Consumer Appointments (DO NOT CHANGE)' calendar, and sends an email to the corresponding
    consumer

    :param credential: (type: CredentialsField) Google OAuth2 Credentials object
    :param rqst_apt_datetime:
    :param consumer_info:
    :param nav_info:
    :param post_errors: (type: list) list of error messages
    :return:
    """

    scheduled_appointment = {}
    if not post_errors:
        try:
            now_date_time = datetime.datetime.utcnow()
            rqst_apt_timestamp = dateutil.parser.parse(rqst_apt_datetime)
            if now_date_time < rqst_apt_timestamp:
                apt_end_timestamp = dateutil.parser.parse(rqst_apt_datetime) + datetime.timedelta(minutes=30)
                service = build_authorized_cal_http_service_object(credential)

                navigator_calendar_found, navigator_calendar_id = check_cal_objects_for_nav_cal(service, post_errors)
                if not navigator_calendar_found:
                    post_errors.append("Navigator calendar not found for this navigator, creating it...")
                    navigator_calendar_id = add_nav_cal_to_google_cals(service, post_errors)

                service = build_authorized_cal_http_service_object(credential)
                nav_apt_args = {"summary": "Navigator ({!s} {!s}) appointment with {!s} {!s}".format(nav_info["First Name"],
                                                                                                     nav_info["Last Name"],
                                                                                                     consumer_info["first_name"],
                                                                                                     consumer_info["last_name"]),
                                "description": "Consumer will be expecting a call at {!s}\nOther Consumer Info:\nFirst Name: {!s}\nLast Name: {!s}\nEmail: {!s}".format(consumer_info["phone"],
                                                                                                                                                                        consumer_info["first_name"],
                                                                                                                                                                        consumer_info["last_name"],
                                                                                                                                                                        consumer_info["email"]),
                                "start": {"dateTime": rqst_apt_datetime + 'Z'},
                                "end": {"dateTime": apt_end_timestamp.isoformat() + 'Z'}
                                }
                try:
                    navigator_appointment_object = service.events().insert(calendarId=navigator_calendar_id, body=nav_apt_args, sendNotifications=True).execute()

                    scheduled_appointment["Navigator Name"] = "{!s} {!s}".format(nav_info["First Name"],nav_info["Last Name"])
                    scheduled_appointment["Navigator Database ID"] = nav_info["Database ID"]
                    scheduled_appointment["Appointment Date and Time"] = rqst_apt_datetime
                    scheduled_appointment["Appointment Title"] = navigator_appointment_object["summary"]
                    scheduled_appointment["Appointment Summary"] = navigator_appointment_object["description"]

                    if "Email" in consumer_info:
                        try:
                            validate_email(consumer_info["email"])
                            send_apt_info_email_to_consumer(consumer_info, nav_info, scheduled_appointment, post_errors)
                        except forms.ValidationError:
                            post_errors.append("Email: {!s} for consumer database id: {!s} must be a valid email address, email to consumer not sent".format(consumer_info["email"], consumer_info["id"]))
                    else:
                        post_errors.append("Consumer with database id: {!s} does not have an email address specified, email to consumer not sent".format(consumer_info["id"]))
                except Exception:
                    post_errors.append("Call to Google failed, Check API call")
            else:
                post_errors.append("{!s} is not a valid datetime. It is before the current datetime".format(rqst_apt_datetime))

        except ValueError:
            post_errors.append("Requested appointment time must be after current time")

    return scheduled_appointment


def send_apt_info_email_to_consumer(consumer_info, nav_info, scheduled_appointment, post_errors):
    """
    This function takes a dictionary populated with data about a consumer appointment with a navigator, and sends a
    confirmation email to the consumer.

    :param consumer_info:
    :param nav_info:
    :param scheduled_appointment:
    :param post_errors: (type: list) list of error messages
    :return:
    """

    try:
        mandrill_client = mandrill.Mandrill('1veuJ5Rt5CtLEDj64ijXIA')
        message_content = "Hello, you have an appointment scheduled with {!s} {!s} at {!s}. They will be contacting you at {!s}. We look forward to speaking with you!".format(nav_info["First Name"], nav_info["Last Name"], scheduled_appointment["Appointment Date and Time"], consumer_info["phone"])
        message = {'auto_html': None,
                     'auto_text': None,
                     'from_email': 'tech@piccares.org',
                     'from_name': 'Patient Innovation Center',
                     'headers': {'Reply-To': nav_info["Email"]},
                     'html': '<p>{!s}</p>'.format(message_content),
                     'important': True,
                     'subject': scheduled_appointment["Appointment Title"],
                     # 'text': 'Example text content',
                     'to': [{'email': consumer_info["email"],
                             'name': '{!s} {!s}'.format(consumer_info["first_name"], consumer_info["last_name"]),
                             'type': 'to'}],}
        result = mandrill_client.messages.send(message=message)
        '''
        [{'_id': 'abc123abc123abc123abc123abc123',
          'email': 'recipient.email@example.com',
          'reject_reason': 'hard-bounce',
          'status': 'sent'}]
        '''

    except mandrill.Error:
        # Mandrill errors are thrown as exceptions
        post_errors.append('A mandrill error occurred')
        # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'


def delete_nav_apt_from_google_calendar(post_data, post_errors):
    """
    This function takes a dictionary populated with data about a consumer appointment with a navigator and deletes it
    from the navigator's 'Navigator-Consumer Appointments (DO NOT CHANGE)' calendar.

    :param post_data: (type: dictionary) dictionary with Patient Assist appointment info
    :param post_errors: (type: list) list of error messages
    :return:
    """

    google_apt_deleted = False

    rqst_nav_id = clean_int_value_from_dict_object(post_data, "root", "Navigator ID", post_errors)
    rqst_apt_datetime = clean_string_value_from_dict_object(post_data, "root", "Appointment Date and Time", post_errors)
    if not isinstance(rqst_apt_datetime, str):
        post_errors.append("{!s} is not a string, Preferred Times must be a string iso formatted date and time".format(str(rqst_apt_datetime)))

    try:
        picstaff_object = PICStaff.objects.get(id=rqst_nav_id)
        credentials_object = CredentialsModel.objects.get(id=picstaff_object)
        nav_info = picstaff_object.return_values_dict()
        if credentials_object.credential.invalid:
            credentials_object.delete()
            post_errors.append('Google Credentials database entry is invalid for the navigator with id: {!s}'.format(str(rqst_nav_id)))
        else:
            service = build_authorized_cal_http_service_object(credentials_object.credential)

            navigator_calendar_found, navigator_calendar_id = check_cal_objects_for_nav_cal(service, post_errors)
            if not navigator_calendar_found:
                post_errors.append("Navigator calendar not found for this navigator, creating it...")
                navigator_calendar_id = add_nav_cal_to_google_cals(service, post_errors)

            google_apt_id = check_google_cal_for_apt(credentials_object, rqst_apt_datetime, post_errors, navigator_calendar_id)

            if google_apt_id:
                google_apt_deleted = send_delete_apt_rqst_to_google(credentials_object, google_apt_id, navigator_calendar_id, post_errors)
            else:
                post_errors.append('Appointment with consumer at {!s}, was not found in Navigator\'s Google Calendar'.format(rqst_apt_datetime))

    except PICStaff.DoesNotExist:
        post_errors.append('Navigator database entry does not exist for the id: {!s}'.format(str(rqst_nav_id)))
    except CredentialsModel.DoesNotExist:
        post_errors.append('Google Credentials database entry does not exist for the navigator with id: {!s}'.format(str(rqst_nav_id)))

    return google_apt_deleted


def check_google_cal_for_apt(credentials_object, rqst_apt_datetime, post_errors, navigator_calendar_id):
    """
    This function takes a dictionary populated with data about a consumer appointment with a navigator and searches the
    navigator's 'Navigator-Consumer Appointments (DO NOT CHANGE)' calendar for the appointment id.

    :param credentials_object: (type: CredentialsModel) picmodels instance that contains Google OAuth2 Credentials object
    :param rqst_apt_datetime:
    :param post_errors: (type: list) list of error messages
    :param navigator_calendar_id:
    :return:
    """

    google_apt_id = None

    try:
        apt_end_timestamp = dateutil.parser.parse(rqst_apt_datetime) + datetime.timedelta(minutes=30)

        if navigator_calendar_id:
            service = build_authorized_cal_http_service_object(credentials_object.credential)
            try:
                event_objects = service.events().list(calendarId=navigator_calendar_id,
                                                      orderBy="startTime",
                                                      singleEvents=True,
                                                      showHiddenInvitations=True,
                                                      timeMin=rqst_apt_datetime + 'Z').execute()["items"]

                google_apt_id = parse_google_events_for_nav_apt(event_objects, rqst_apt_datetime)
            except Exception:
                post_errors.append("Call to Google failed, Check API call")

    except ValueError:
        post_errors.append("{!s} is not a properly iso formatted date and time, Preferred Times must be a string iso formatted date and time".format(rqst_apt_datetime))

    return google_apt_id


def parse_google_events_for_nav_apt(event_objects, rqst_apt_datetime):
    """
    This function takes a list of Google event objects from the navigator's 'Navigator-Consumer Appointments (DO NOT CHANGE)'
    calendar and returns the appointment id whose start time matches the given datetime.

    :param event_objects:
    :param rqst_apt_datetime:
    :return:
    """

    google_apt_id = None

    for event in event_objects:
        if event["start"]["dateTime"] == rqst_apt_datetime + "Z":
            google_apt_id = event["id"]
            break

    return google_apt_id


def send_delete_apt_rqst_to_google(credentials_object, google_apt_id, navigator_calendar_id, post_errors):
    """
    This function takes a given appointment id and deletes it from the calendar corresponding to the given calendar
    id

    :param credentials_object: (type: CredentialsModel) picmodels instance that contains Google OAuth2 Credentials object
    :param google_apt_id:
    :param navigator_calendar_id:
    :param post_errors: (type: list) list of error messages
    :return:
    """

    google_apt_deleted = False

    service = build_authorized_cal_http_service_object(credentials_object.credential)
    try:
        service.events().delete(calendarId=navigator_calendar_id, eventId=google_apt_id, sendNotifications=True).execute()
        google_apt_deleted = True
    except Exception:
        post_errors.append("Delete Appointment request for Calendar ID: {!s} and Event ID: {!s} failed".format(navigator_calendar_id, google_apt_id))

    return google_apt_deleted


def get_preferred_nav_apts(rqst_preferred_times, valid_rqst_preferred_times_timestamps, post_errors):
    """
    This function takes a list of preferred appointment times and returns a list of appointment objects that correspond
    to the given times.

    :param rqst_preferred_times:
    :param valid_rqst_preferred_times_timestamps:
    :param post_errors: (type: list) list of error messages
    :return:
    """

    preferred_appointments = []
    oldest_preferred_time_timestamp = min(valid_rqst_preferred_times_timestamps)
    max_preferred_time_timestamp = max(valid_rqst_preferred_times_timestamps) + datetime.timedelta(hours=1)

    nav_free_busy_list = get_nav_free_busy_times(oldest_preferred_time_timestamp, max_preferred_time_timestamp, post_errors)

    for preferred_time_iso_string in rqst_preferred_times:
        shuffle(nav_free_busy_list)
        preferred_appointments_list = []

        if not isinstance(preferred_time_iso_string, str):
            post_errors.append("{!s} is not a string, Preferred Times must be a string iso formatted date and time".format(str(preferred_time_iso_string)))
        else:
            try:
                preferred_time_timestamp = dateutil.parser.parse(preferred_time_iso_string).replace(tzinfo=pytz.UTC)

                for nav_free_busy_entry in nav_free_busy_list:
                    nav_info = nav_free_busy_entry[0]
                    nav_busy_list = nav_free_busy_entry[1]
                    if not nav_busy_list:
                        preferred_appointments_list.append(create_navigator_apt_entry(nav_info, preferred_time_timestamp))
                        break
                    else:
                        nav_is_busy = False
                        for busy_time_dict in nav_busy_list:
                            start_date_time = dateutil.parser.parse(busy_time_dict['start'])
                            end_date_time = dateutil.parser.parse(busy_time_dict['end'])
                            if start_date_time <= preferred_time_timestamp < end_date_time:
                                nav_is_busy = True
                                break

                        if not nav_is_busy:
                            preferred_appointments_list.append(create_navigator_apt_entry(nav_info, preferred_time_timestamp))
                            break

            except ValueError:
                post_errors.append("{!s} is not a properly iso formatted date and time, Preferred Times must be a string iso formatted date and time".format(preferred_time_iso_string))

        preferred_appointments.append(preferred_appointments_list)

    return preferred_appointments


def get_next_available_nav_apts(post_errors):
    """
    This function returns an list containing appointment objects that correspond to the next available times starting
    from when the function gets called.

    :param post_errors: (type: list) list of error messages
    :return:
    """

    next_available_appointments = []

    now_date_time = datetime.datetime.utcnow()
    earliest_available_date_time = get_earliest_available_apt_datetime(now_date_time)

    end_of_next_b_day_date_time = earliest_available_date_time + BDay(1)
    end_of_next_b_day_date_time = end_of_next_b_day_date_time.replace(hour=23, minute=0, second=0, microsecond=0)

    credentials_objects = CredentialsModel.objects.all()
    if credentials_objects:
        while not next_available_appointments:
            possible_appointment_times = get_possible_appointments_range(earliest_available_date_time, end_of_next_b_day_date_time)
            nav_free_busy_list = get_nav_free_busy_times(earliest_available_date_time, end_of_next_b_day_date_time, post_errors)

            for appointment_time in possible_appointment_times:
                shuffle(nav_free_busy_list)

                for nav_free_busy_entry in nav_free_busy_list:
                    nav_info = nav_free_busy_entry[0]
                    nav_busy_list = nav_free_busy_entry[1]
                    if not nav_busy_list:
                        next_available_appointments.append(create_navigator_apt_entry(nav_info, appointment_time))
                        break
                    else:
                        nav_is_busy = False
                        for busy_time_dict in nav_busy_list:
                            start_date_time = dateutil.parser.parse(busy_time_dict['start'])
                            end_date_time = dateutil.parser.parse(busy_time_dict['end'])
                            if start_date_time <= appointment_time < end_date_time:
                                nav_is_busy = True
                                break

                        if not nav_is_busy:
                            next_available_appointments.append(create_navigator_apt_entry(nav_info, appointment_time))
                            break

            if not next_available_appointments:
                earliest_available_date_time = end_of_next_b_day_date_time + BDay(1)
                earliest_available_date_time = earliest_available_date_time.replace(hour=15, minute=0, second=0, microsecond=0)

                end_of_next_b_day_date_time = earliest_available_date_time + BDay(1)
                end_of_next_b_day_date_time = end_of_next_b_day_date_time.replace(hour=23, minute=0, second=0, microsecond=0)
    else:
        post_errors.append("No Navigators with Authorized credentials to query from. Next Available Appointments will be empty.")

    return next_available_appointments


def create_navigator_apt_entry(nav_info, appointment_timestamp):
    """
    This function takes a dictionary popluated with navigator information and an appointment timestamp and creates
    an dictionary containing appointment information corresponding to the information given.

    :param nav_info:
    :param appointment_timestamp:
    :return:
    """

    next_available_apt_entry = {"Navigator Name": "{!s} {!s}".format(nav_info["First Name"],nav_info["Last Name"]),
                                "Navigator Database ID": nav_info["Database ID"],
                                "Appointment Date and Time": appointment_timestamp.isoformat()[:-6],
                                "Schedule Appointment Link": "http://picbackend.herokuapp.com/v1/scheduleappointment/?nav_id={!s}".format(str(nav_info["Database ID"])),
                                }

    return next_available_apt_entry


def get_earliest_available_apt_datetime(now_date_time):
    """
    This function takes a datetime object and returns the earliest possible business datetime starting from the given
    datetime object.

    :param now_date_time:
    :return:
    """

    if not isbday(now_date_time):
        earliest_available_date_time = now_date_time + BDay(1)
        earliest_available_date_time = earliest_available_date_time.replace(hour=15, minute=0, second=0, microsecond=0)
    else:
        current_time = datetime.time(hour=now_date_time.hour, minute=now_date_time.minute, second=now_date_time.second, microsecond=now_date_time.microsecond)

        if current_time > END_OF_BUSINESS_TIMESTAMP:
            earliest_available_date_time = now_date_time + BDay(1)
            earliest_available_date_time = earliest_available_date_time.replace(hour=15, minute=0, second=0, microsecond=0)
        elif current_time < START_OF_BUSINESS_TIMESTAMP:
            earliest_available_date_time = now_date_time.replace(hour=15, minute=0, second=0, microsecond=0)
        else:
            earliest_available_date_time = now_date_time

    return earliest_available_date_time


def get_possible_appointments_range(earliest_available_date_time, end_of_next_b_day_date_time):
    """
    This function takes a start and an end of next business day datetime, and returns a list of datetimes in 15 min
    intervals that are within business time.

    :param earliest_available_date_time:
    :param end_of_next_b_day_date_time:
    :return:
    """

    earliest_available_time = datetime.time(hour=earliest_available_date_time.hour, minute=earliest_available_date_time.minute, second=earliest_available_date_time.second, microsecond=earliest_available_date_time.microsecond)
    possible_appointment_times = []

    day_1_appointment_timesstamps = bdate_range(start=earliest_available_date_time, end=earliest_available_date_time + datetime.timedelta(days=1), freq='30min', tz=tzutc())
    day_1_appointment_timesstamps = day_1_appointment_timesstamps.tolist()

    for timestamp in day_1_appointment_timesstamps:
        timestamp_time = datetime.time(hour=timestamp.hour, minute=timestamp.minute, second=timestamp.second, microsecond=timestamp.microsecond)
        if earliest_available_time < timestamp_time < END_OF_BUSINESS_TIMESTAMP:
            possible_appointment_times.append(timestamp)

    day_2_appointment_timesstamps = bdate_range(start=end_of_next_b_day_date_time, end=end_of_next_b_day_date_time + datetime.timedelta(days=1), freq='30min', tz=tzutc())
    day_2_appointment_timesstamps = day_2_appointment_timesstamps.tolist()

    for timestamp in day_2_appointment_timesstamps:
        timestamp_time = datetime.time(hour=timestamp.hour, minute=timestamp.minute, second=timestamp.second, microsecond=timestamp.microsecond)
        if START_OF_BUSINESS_TIMESTAMP <= timestamp_time < END_OF_BUSINESS_TIMESTAMP:
            possible_appointment_times.append(timestamp)

    return possible_appointment_times


def get_nav_free_busy_times(start_timestamp, end_timestamp, post_errors):
    """
    This function takes a start and an end timestamp and returns an object which contains intervals where the
    navigators who have authorized credentials are busy.

    :param start_timestamp:
    :param end_timestamp:
    :param post_errors: (type: list) list of error messages
    :return:
    """

    nav_cal_list_dict = get_nav_cal_lists(post_errors)

    nav_free_busy_list = get_free_busy_list(start_timestamp, end_timestamp, nav_cal_list_dict, post_errors)

    return nav_free_busy_list


def get_nav_cal_lists(post_errors):
    """
    This function retrieves the list of Google calendars for all navigators who have authorized google credentials.

    :param post_errors: (type: list) list of error messages
    :return:
    """

    nav_cal_list_dict = {}

    def add_cal_list_entry(request_id, response, exception):
        nav_cal_list_dict[request_id] = response["items"]

    # build batch request
    cal_list_batch = BatchHttpRequest()

    credentials_objects = list(CredentialsModel.objects.all())
    while credentials_objects:
        credentials_object = credentials_objects.pop()
        nav_object = credentials_object.id

        if credentials_object.credential.invalid:
            credentials_object.delete()
        else:
            nav_cal_list_dict[str(nav_object.id)] = []

            # Obtain valid credential and use it to build authorized service object for given navigator
            credential = credentials_object.credential
            service = build_authorized_cal_http_service_object(credential)

            cal_list_batch.add(service.calendarList().list(showHidden=True), callback=add_cal_list_entry, request_id=str(nav_object.id))

    try:
        cal_list_batch.execute()
    except Exception:
        post_errors.append("Batch call to Google failed, Check API call")

    return nav_cal_list_dict


def get_free_busy_list(start_timestamp, end_timestamp, nav_cal_list_dict, post_errors):
    """
    This function retrieves the busy times for a given interval for all navigators who have authorized credentials from
    Google.

    :param start_timestamp:
    :param end_timestamp:
    :param nav_cal_list_dict:
    :param post_errors: (type: list) list of error messages
    :return:
    """

    nav_free_busy_dict = {}
    nav_free_busy_list = []

    def add_free_busy_entry(request_id, response, exception):
        for cals_key, calendar_object in response["calendars"].items():
            busy_list = calendar_object["busy"]
            if busy_list:
                for busy_entry in busy_list:
                    nav_free_busy_dict[request_id].append(busy_entry)

    # build batch request
    # Each HTTP connection that your application makes results in a certain amount of overhead. This library supports
    # batching, to allow your application to put several API calls into a single HTTP request. Examples of situations
    # when you might want to use batching:

    # You have many small requests to make and would like to minimize HTTP request overhead.
    # A user made changes to data while your application was offline, so your application needs to synchronize its
    # local data with the server by sending a lot of updates and deletes.
    # Note: You're limited to 1000 calls in a single batch request. If you need to make more calls than that, use
    # multiple batch requests
    free_busy_batch = BatchHttpRequest()

    credentials_objects = list(CredentialsModel.objects.all())
    while credentials_objects:
        credentials_object = credentials_objects.pop()
        nav_object = credentials_object.id

        if credentials_object.credential.invalid:
            credentials_object.delete()
        else:
            nav_free_busy_dict[str(nav_object.id)] = []

            #Obtain valid credential and use it to build authorized service object for given navigator
            credential = credentials_object.credential
            service = build_authorized_cal_http_service_object(credential)

            nav_cal_list_object = nav_cal_list_dict[str(nav_object.id)]
            items_list = []
            for nav_cal_object in nav_cal_list_object:
                items_entry = {"id": nav_cal_object["id"]}
                items_list.append(items_entry)

            free_busy_args = {"timeMin": start_timestamp.isoformat() + 'Z', # 'Z' indicates UTC time
                              "timeMax": end_timestamp.isoformat() + 'Z',
                              "items": items_list}
            free_busy_batch.add(service.freebusy().query(body=free_busy_args), callback=add_free_busy_entry, request_id=str(nav_object.id))

    try:
        free_busy_batch.execute()

        for key, value in nav_free_busy_dict.items():
            nav_free_busy_list.append([PICStaff.objects.get(id=int(key)).return_values_dict(), value])
    except Exception:
        post_errors.append("Batch call to Google failed, Check API call")

    return nav_free_busy_list


def get_nav_scheduled_appointments(nav_info, credentials_object, rqst_errors):
    """
    This function retrieves all the scheduled appointments from a given navigator's '"Navigator-Consumer Appointments (DO NOT CHANGE)"'
    Google calendar.

    :param nav_info:
    :param credentials_object: (type: CredentialsModel) picmodels instance that contains Google OAuth2 Credentials object
    :param rqst_errors: (type: list) list of error messages
    :return:
    """

    scheduled_appointment_list = []
    credential = credentials_object.credential

    service = build_authorized_cal_http_service_object(credential)

    try:
        nav_cal_list = service.calendarList().list(showHidden=True).execute()["items"]
        nav_cal_id = None
        for calendar in nav_cal_list:
            calendar_name = calendar["summary"]
            if calendar_name == "Navigator-Consumer Appointments (DO NOT CHANGE)":
                nav_cal_id = calendar["id"]
        if not nav_cal_id:
            rqst_errors.append("Navigator-Consumer Appointments not found in Navigator's Google CalendarList")

        if not rqst_errors:
            service = build_authorized_cal_http_service_object(credential)

            try:
                nav_cal_events = service.events().list(calendarId=nav_cal_id,
                                                       orderBy="startTime",
                                                       showHiddenInvitations=True,
                                                       singleEvents=True,
                                                       timeMin=datetime.datetime.utcnow().isoformat() + 'Z').execute()["items"]

                if nav_cal_events:
                    for cal_event in nav_cal_events:
                        scheduled_appointment_entry = {"Navigator Name": "{!s} {!s}".format(nav_info["First Name"],nav_info["Last Name"]),
                                                       "Navigator Database ID": nav_info["Database ID"],
                                                       "Appointment Date and Time": cal_event["start"]["dateTime"][:-1],
                                                       "Appointment Summary": None}
                        if "description" in cal_event:
                            scheduled_appointment_entry["Appointment Summary"] = cal_event["description"]
                        scheduled_appointment_list.append(scheduled_appointment_entry)
                else:
                    rqst_errors.append("No scheduled appointments in navigator's 'Navigator-Consumer Appointments' calendar")
            except Exception:
                rqst_errors.append("Call to Google failed for Navigator's Calendar Events, Check API call")
    except Exception:
        rqst_errors.append("Call to Google failed for Navigator's Calendar List, Check API call")

    return scheduled_appointment_list
