"""
Defines views that are mapped to url configurations
"""

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect, render_to_response, render
from django import forms
from django.db import models, IntegrityError
from django.contrib.auth.models import User
from picproject.forms import AssessmentFormOne, AssessmentFormTwo, UserCreateForm
from picmodels.models import PICUser, Appointment, Location, PICConsumer, PICStaff, MetricsSubmission
import datetime, json, sys, re
from django.views.decorators.csrf import csrf_exempt


# defines view for home page
def index(request):
    return render(request, "home_page.html")


# defines view for registration page
def registration(request):
    if request.method == 'POST':
        form_data = request.POST.copy()
        form_data['date_joined'] = datetime.date.today()
        form = UserCreateForm(form_data)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/memberlist/")
    else:
        form = UserCreateForm()
    return render(request, "registration.html", {'form': form})


# defines view for member list display page
def memberlist(request):
    all_members = PICUser.objects.all()
    return render(request, "member_list.html", {'member_list': all_members})


# defines view for part 1 of risk assessment page
def risk_assessment(request):
    if request.method == 'POST':
        post_data = request.POST
        form_one = AssessmentFormOne(post_data)
        if form_one.is_valid():
            cd = form_one.cleaned_data
            request.session['form_data'] = cd
            return HttpResponseRedirect('/riskassessment/next/')
    else:
        form_one = AssessmentFormOne()
    return render(request, 'assessment.html', {'form_one': form_one})


# defines view for part 2 of risk assessment page
def risk_assessment_2(request):
    form_data = request.session.get('form_data')
    if form_data:
        for key in form_data:
            form_data[key] = int(form_data[key])
    else:
        raise Http404('need old post data')

    if request.method == 'POST':
        current_post_data = request.POST
        form_one = AssessmentFormTwo(form_data, current_post_data)
        if form_one.is_valid():
            cd = form_one.cleaned_data
            health_risk = 0
            for key in form_data:
                answer = form_data[key]
                if key == 'is_employed' or key == 'has_insurance' or key == 'has_primary_doctor':
                    if answer == 0:
                        health_risk += 1
                else:
                    if answer == 1:
                        health_risk += 1
            for key in cd:
                if int(cd[key]) == 1:
                    health_risk += 1
            health_risk_score = (float(health_risk) / 11) * 100
            health_risk_string = str(int(health_risk_score))
            return render(request, 'assessment_score.html', {'score': health_risk_string})
    else:
        form_one = AssessmentFormTwo(previous_form_data=form_data)
        return render(request, 'assessment_2.html', {'form_one': form_one})

    return render(request, 'assessment_2.html', {'form_one': form_one})


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
            print error_message
            sys.stdout.flush()
            # for message in post_errors:
            #     sys.stdout.write(message + sys.argv[1].decode("string_escape"))

            # response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
            # # response['Access-Control-Allow-Origin'] = "*"
            # return response

    # elif request.method == "OPTIONS":
    #     response = HttpResponse("")
    #     response['Access-Control-Allow-Origin'] = "*"
    #     response['Access-Control-Allow-Methods'] = "POST, OPTIONS, GET"
    #     response['Access-Control-Allow-Headers'] = "X-Requested-With"
    #     response['Access-Control-Max-Age'] = "1800"
    #     return response

    # if a GET request is made, add error message to response data
    else:
        response_raw_data["status"]["Error Code"] = 1
        post_errors.append("Request needs POST data")
        response_raw_data["status"]["Errors"] = post_errors
        for message in post_errors:
            print message
        sys.stdout.flush()

            # response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
            # # response['Access-Control-Allow-Origin'] = "*"
            # return response

    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response


# defines view for member list display page
def appointment_viewing_handler(request):
    all_appointments = Appointment.objects.all()
    return render(request, 'appointment_list.html', {'appointment_list': all_appointments})


# defines view for saving scheduled appointments to the database
@csrf_exempt
def staff_submission_handler(request):
    # initialize dictionary for response data, including parsing errors
    response_raw_data = {'status': {"Error Code": 0, "Version": 1.0}}
    post_errors = []

    if request.method == 'POST' or request.is_ajax():
        post_data = request.body
        post_json = json.loads(post_data)

        # Code to parse POSTed json request
        rqst_usr_email = clean_json_string_input(post_json, "root", "Email", post_errors)
        rqst_usr_f_name = clean_json_string_input(post_json, "root", "First Name", post_errors)
        rqst_usr_l_name = clean_json_string_input(post_json, "root", "Last Name", post_errors)
        rqst_county = clean_json_string_input(post_json, "root", "User County", post_errors)
        rqst_usr_type = clean_json_string_input(post_json, "root", "User Type", post_errors)

        # if there are no parsing errors, get or create database entries for consumer, location, and point of contact
        # create and save database entry for appointment
        if len(post_errors) == 0:
            usr_rqst_values = {"first_name": rqst_usr_f_name,
                               "last_name": rqst_usr_l_name,
                               "type": rqst_usr_type,
                               "county": rqst_county,}
            user_instance, user_instance_created = PICStaff.objects.get_or_create(email=rqst_usr_email,
                                                                                  defaults=usr_rqst_values)
            if not user_instance_created:
                post_errors.append('Staff database entry already exists for the email: {!s}'.format(rqst_usr_email))
                response_raw_data["status"]["Error Code"] = 1
                response_raw_data["status"]["Errors"] = post_errors

                for message in post_errors:
                    print message
                sys.stdout.flush()
            else:
                response_raw_data['Data'] = {"Database ID": user_instance.id}

        # add parsing errors to response dictionary
        else:
            response_raw_data["status"]["Error Code"] = 1
            response_raw_data["status"]["Errors"] = post_errors

            for message in post_errors:
                print message
                sys.stdout.flush()

                # response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
                # response['Access-Control-Allow-Origin'] = "*"
                # return response

    # elif request.method == "OPTIONS":
    #     response = HttpResponse("")
    #     response['Access-Control-Allow-Origin'] = "*"
    #     response['Access-Control-Allow-Methods'] = "POST, OPTIONS, GET"
    #     response['Access-Control-Allow-Headers'] = "X-Requested-With"
    #     response['Access-Control-Max-Age'] = "1800"
    #     return response

    # if a GET request is made, add error message to response data
    else:
        response_raw_data["status"]["Error Code"] = 1
        post_errors.append("Request needs POST data")
        response_raw_data["status"]["Errors"] = post_errors
        for message in post_errors:
            print message
        sys.stdout.flush()

            # response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
            # response['Access-Control-Allow-Origin'] = "*"
            # return response

    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response


# defines view for saving scheduled appointments to the database
@csrf_exempt
def metrics_submission_handler(request):
    # initialize dictionary for response data, including parsing errors
    response_raw_data = {'status': {"Error Code": 0, "Version": 1.0}}
    post_errors = []

    if request.method == 'POST' or request.is_ajax():
        post_data = request.body
        post_json = json.loads(post_data)

        # Code to parse POSTed json request
        rqst_usr_email = clean_json_string_input(post_json, "root", "Email", post_errors)
        rqst_usr_type = clean_json_string_input(post_json, "root", "User Type", post_errors)

        consumer_metrics = clean_dict_input(post_json, "root", "Consumer Metrics", post_errors)
        if consumer_metrics is not None:
            consumer_metrics = post_json["Consumer Metrics"]

            rqst_cons_rec_edu = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Received Education",
                                                     post_errors)
            rqst_cons_app_maid = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Applied Medicaid",
                                                      post_errors)
            rqst_cons_sel_qhp = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Selected QHP", post_errors)
            rqst_cons_enr_shop = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Enrolled SHOP",
                                                      post_errors)
            rqst_cons_ref_maidorchip = clean_json_int_input(consumer_metrics, "Consumer Metrics",
                                                            "Referred Medicaid or CHIP", post_errors)
            rqst_cons_ref_shop = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Referred SHOP",
                                                      post_errors)
            rqst_cons_filed_exemptions = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Filed Exemptions",
                                                              post_errors)
            rqst_cons_rec_postenr_support = clean_json_int_input(consumer_metrics, "Consumer Metrics",
                                                                 "Received Post-Enrollment Support", post_errors)
            rqst_cons_trends = clean_json_string_input(consumer_metrics, "Consumer Metrics", "Trends", post_errors,
                                                       empty_string_allowed=True, none_allowed=True)
            rqst_cons_success_story = clean_json_string_input(consumer_metrics, "Consumer Metrics", "Success Story",
                                                              post_errors)
            rqst_cons_hard_or_diff = clean_json_string_input(consumer_metrics, "Consumer Metrics",
                                                             "Hardship or Difficulty", post_errors)
            rqst_usr_comments = clean_json_string_input(consumer_metrics, "Consumer Metrics", "Comments", post_errors,
                                                        empty_string_allowed=True, none_allowed=True)
            rqst_usr_outr_stkehol_act = clean_json_string_input(consumer_metrics, "Consumer Metrics",
                                                                "Outreach and Stakeholder Activities", post_errors,
                                                                empty_string_allowed=True, none_allowed=True)
            rqst_metrics_county = clean_json_string_input(consumer_metrics, "Consumer Metrics", "County", post_errors)

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

            if rqst_usr_type == "IPC":
                rqst_cons_apts_sched = clean_json_int_input(consumer_metrics, "Consumer Metrics",
                                                            "Appointments Scheduled", post_errors)
                rqst_cons_confirm_calls = clean_json_int_input(consumer_metrics, "Consumer Metrics",
                                                               "Confirmation Calls", post_errors)
                rqst_cons_apts_held = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Appointments Held",
                                                           post_errors)
                rqst_cons_apts_over_hour = clean_json_int_input(consumer_metrics, "Consumer Metrics",
                                                                "Appointments Over Hour", post_errors)
                rqst_cons_apts_cplx_market = clean_json_int_input(consumer_metrics, "Consumer Metrics",
                                                                  "Appointments Complex Market", post_errors)
                rqst_cons_apts_cplx_maid = clean_json_int_input(consumer_metrics, "Consumer Metrics",
                                                                "Appointments Complex Medicaid", post_errors)
                rqst_cons_apts_postenr_assis = clean_json_int_input(consumer_metrics, "Consumer Metrics",
                                                                    "Appointments Post-Enrollment Assistance",
                                                                    post_errors)
                rqst_cons_apts_over_3_hours = clean_json_int_input(consumer_metrics, "Consumer Metrics",
                                                                   "Appointments Over 3 Hours", post_errors)

        # if there are no parsing errors, get or create database entries for consumer, location, and point of contact
        # create and save database entry for appointment
        if len(post_errors) == 0:
            # usr_rqst_values = {"first_name": rqst_usr_f_name,
            #                    "last_name": rqst_usr_l_name,
            #                    "type": rqst_usr_type,}
            # user_instance, user_instance_created = PICStaff.objects.get_or_create(email=rqst_usr_email,
            #                                                                       defaults=usr_rqst_values)
            try:
                user_instance = PICStaff.objects.get(email__iexact=rqst_usr_email)

                new_metrics_instance = MetricsSubmission(staff_member=user_instance,
                                                         received_education=rqst_cons_rec_edu,
                                                         applied_medicaid=rqst_cons_app_maid,
                                                         selected_qhp=rqst_cons_sel_qhp,
                                                         enrolled_shop=rqst_cons_enr_shop,
                                                         ref_medicaid_or_chip=rqst_cons_ref_maidorchip,
                                                         ref_shop=rqst_cons_ref_shop,
                                                         filed_exemptions=rqst_cons_filed_exemptions,
                                                         rec_postenroll_support=rqst_cons_rec_postenr_support,
                                                         trends=rqst_cons_trends,
                                                         success_story=rqst_cons_success_story,
                                                         hardship_or_difficulty=rqst_cons_hard_or_diff,
                                                         comments=rqst_usr_comments,
                                                         outreach_stakeholder_activity=rqst_usr_outr_stkehol_act,
                                                         county=rqst_metrics_county,
                                                         submission_date=metrics_date,)

                if rqst_usr_type == "IPC":
                    new_metrics_instance.appointments_scheduled = rqst_cons_apts_sched
                    new_metrics_instance.confirmation_calls = rqst_cons_confirm_calls
                    new_metrics_instance.appointments_held = rqst_cons_apts_held
                    new_metrics_instance.appointments_over_hour = rqst_cons_apts_over_hour
                    new_metrics_instance.appointments_over_three_hours = rqst_cons_apts_over_3_hours
                    new_metrics_instance.appointments_cmplx_market = rqst_cons_apts_cplx_market
                    new_metrics_instance.appointments_cmplx_medicaid = rqst_cons_apts_cplx_maid
                    new_metrics_instance.appointments_postenroll_assistance = rqst_cons_apts_postenr_assis

                new_metrics_instance.save()
            except models.ObjectDoesNotExist:
                response_raw_data["status"]["Error Code"] = 1
                post_errors.append("Staff database entry does not exist for email: {!s}".format(rqst_usr_email))
                response_raw_data["status"]["Errors"] = post_errors
                for message in post_errors:
                    print message
                sys.stdout.flush()

        # add parsing errors to response dictionary
        else:
            response_raw_data["status"]["Error Code"] = 1
            response_raw_data["status"]["Errors"] = post_errors

            for message in post_errors:
                print message
                sys.stdout.flush()

                # response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
                # response['Access-Control-Allow-Origin'] = "*"
                # return response

    # elif request.method == "OPTIONS":
    #     response = HttpResponse("")
    #     response['Access-Control-Allow-Origin'] = "*"
    #     response['Access-Control-Allow-Methods'] = "POST, OPTIONS, GET"
    #     response['Access-Control-Allow-Headers'] = "X-Requested-With"
    #     response['Access-Control-Max-Age'] = "1800"
    #     return response

    # if a GET request is made, add error message to response data
    else:
        response_raw_data["status"]["Error Code"] = 1
        post_errors.append("Request needs POST data")
        response_raw_data["status"]["Errors"] = post_errors
        for message in post_errors:
            print message
        sys.stdout.flush()

            # response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
            # response['Access-Control-Allow-Origin'] = "*"
            # return response

    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response


# defines view for returning staff data from api requests
def staff_api_handler(request):
    rqst_params = request.GET

    response_raw_data = {'Status': {"Error Code": 0, "Version": 1.0}}
    rqst_errors = []

    if 'lname' in rqst_params and 'fname' in rqst_params:
        rqst_first_name = rqst_params['fname']
        rqst_last_name = rqst_params['lname']
        staff_objects = PICStaff.objects.filter(first_name__iexact=rqst_first_name, last_name__iexact=rqst_last_name)
        if len(staff_objects) > 0:
            staff_member_dict = {}
            rqst_full_name = rqst_first_name + " " + rqst_last_name
            for staff_member in staff_objects:
                if rqst_full_name not in staff_member_dict:
                    staff_member_dict[rqst_full_name] = [staff_member.return_values_dict()]
                else:
                    staff_member_dict[rqst_full_name].append(staff_member.return_values_dict())
            response_raw_data["Data"] = staff_member_dict
        else:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('Staff Member with name: {!s} {!s} not found in database'.format(rqst_first_name,
                                                                                                rqst_last_name))
    elif 'email' in rqst_params:
        rqst_email = rqst_params['email']
        list_of_emails = re.findall("[\w.'-@]+", rqst_email)
        staff_dict = {}
        for email in list_of_emails:
            staff_members = PICStaff.objects.filter(email__iexact=email)
            for staff_member in staff_members:
                if email not in staff_dict:
                    staff_dict[email] = [staff_member.return_values_dict()]
                else:
                    staff_dict[email].append(staff_member.return_values_dict())
        if len(staff_dict) > 0:
            response_raw_data["Data"] = staff_dict
            for email in list_of_emails:
                if email not in staff_dict:
                    if response_raw_data['Status']['Error Code'] != 2:
                        response_raw_data['Status']['Error Code'] = 2
                    rqst_errors.append('Staff Member with email: {!s} not found in database'.format(email))
        else:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('Staff Member with emails(s): {!s} not found in database'.format(rqst_email))

    elif 'fname' in rqst_params:
        rqst_first_name = rqst_params['fname']
        list_of_first_names = re.findall("[\w.'-]+", rqst_first_name)
        staff_dict = {}
        for first_name in list_of_first_names:
            staff_members = PICStaff.objects.filter(first_name__iexact=first_name)
            for staff_member in staff_members:
                if first_name not in staff_dict:
                    staff_dict[first_name] = [staff_member.return_values_dict()]
                else:
                    staff_dict[first_name].append(staff_member.return_values_dict())
        if len(staff_dict) > 0:
            response_raw_data["Data"] = staff_dict
            for name in list_of_first_names:
                if name not in staff_dict:
                    if response_raw_data['Status']['Error Code'] != 2:
                        response_raw_data['Status']['Error Code'] = 2
                    rqst_errors.append('Staff Member with first name: {!s} not found in database'.format(name))
        else:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('Staff Member with first name(s): {!s} not found in database'.format(rqst_first_name))

    elif 'lname' in rqst_params:
        rqst_last_name = rqst_params['lname']
        list_of_last_names = re.findall("[\w.'-]+", rqst_last_name)
        staff_dict = {}
        for last_name in list_of_last_names:
            staff_members = PICStaff.objects.filter(last_name__iexact=last_name)
            for staff_member in staff_members:
                if last_name not in staff_dict:
                    staff_dict[last_name] = [staff_member.return_values_dict()]
                else:
                    staff_dict[last_name].append(staff_member.return_values_dict())
        if len(staff_dict) > 0:
            response_raw_data["Data"] = staff_dict
            for name in list_of_last_names:
                if name not in staff_dict:
                    if response_raw_data['Status']['Error Code'] != 2:
                        response_raw_data['Status']['Error Code'] = 2
                    rqst_errors.append('Staff Member with last name: {!s} not found in database'.format(name))
        else:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('Staff Member with last name(s): {!s} not found in database'.format(rqst_last_name))

    elif 'id' in rqst_params:
        rqst_staff_id = rqst_params['id']

        if rqst_staff_id == "all":
            all_staff_members = PICStaff.objects.all()
            staff_member_dict = {}
            for staff_member in all_staff_members:
                staff_member_dict[staff_member.id] = staff_member.return_values_dict()
            response_raw_data["Data"] = staff_member_dict
        else:
            list_of_ids = re.findall("\d+", rqst_staff_id)
            if len(list_of_ids) > 0:
                for indx, element in enumerate(list_of_ids):
                    list_of_ids[indx] = int(element)
                staff_members = PICStaff.objects.filter(id__in=list_of_ids)
                if len(staff_members) > 0:
                    staff_dict = {}
                    for staff_member in staff_members:
                        staff_dict[staff_member.id] = staff_member.return_values_dict()
                    response_raw_data["Data"] = staff_dict

                    for staff_id in list_of_ids:
                        if staff_id not in staff_dict:
                            if response_raw_data['Status']['Error Code'] != 2:
                                response_raw_data['Status']['Error Code'] = 2
                            rqst_errors.append('Staff Member with id: {!s} not found in database'.format(str(staff_id)))
                else:
                    response_raw_data['Status']['Error Code'] = 1
                    rqst_errors.append('No staff members found for database ID(s): ' + rqst_staff_id)
            else:
                response_raw_data['Status']['Error Code'] = 1
                rqst_errors.append('No valid staff IDs provided in request (must be integers)')

    else:
        response_raw_data['Status']['Error Code'] = 1
        rqst_errors.append('No Valid Parameters')

    response_raw_data["Status"]["Errors"] = rqst_errors
    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response


# defines function to group metrics by given parameter
def group_metrics(metrics_dict, grouping_parameter):
    return_dict = {}
    if grouping_parameter == "County":
        for staff_key, staff_dict in metrics_dict.iteritems():
            for metrics_entry in staff_dict["Metrics Data"]:
                if metrics_entry[grouping_parameter] not in return_dict:
                    return_dict[metrics_entry[grouping_parameter]] = {staff_key: {"Metrics Data": [metrics_entry],
                                                                      "Staff Information": staff_dict["Staff Information"]}}
                else:
                    if staff_key not in return_dict[metrics_entry[grouping_parameter]]:
                        return_dict[metrics_entry[grouping_parameter]][staff_key] = {"Metrics Data": [metrics_entry],
                                                                                     "Staff Information": staff_dict["Staff Information"]}
                    else:
                        return_dict[metrics_entry[grouping_parameter]][staff_key]["Metrics Data"].append(metrics_entry)
    return return_dict


# defines view for returning metrics data from api requests
def metrics_api_handler(request):
    rqst_params = request.GET
    if "county" in rqst_params:
        rqst_counties = rqst_params["county"]
        list_of_counties = re.findall("[\w. '-]+", rqst_counties)
    else:
        list_of_counties = None

    response_raw_data = {'Status': {"Error Code": 0, "Version": 1.0}}
    rqst_errors = []

    if 'id' in rqst_params:
        rqst_staff_id = str(rqst_params["id"])
        if rqst_staff_id == "all":
            if list_of_counties is not None:
                metrics_submissions = []
                for county in list_of_counties:
                    county_metrics = MetricsSubmission.objects.filter(county__iexact=county)
                    for metrics_entry in county_metrics:
                        metrics_submissions.append(metrics_entry)
            else:
                metrics_submissions = MetricsSubmission.objects.all()

            if len(metrics_submissions) > 0:
                metrics_dict = {}
                for metrics_submission in metrics_submissions:
                    if metrics_submission.staff_member_id not in metrics_dict:
                        metrics_dict[metrics_submission.staff_member_id] = {"Metrics Data": [metrics_submission.return_values_dict()]}
                        metrics_dict[metrics_submission.staff_member_id]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                    else:
                        metrics_dict[metrics_submission.staff_member_id]["Metrics Data"].append(metrics_submission.return_values_dict())
                if "groupby" in rqst_params:
                    if rqst_params["groupby"] == "county" or rqst_params["groupby"] == "County":
                        metrics_dict = group_metrics(metrics_dict, "County")
                        metrics_list = []
                        for metrics_key, metrics_entry in metrics_dict.iteritems():
                            metrics_list.append(metrics_entry)
                        response_raw_data["Data"] = metrics_list
                        # response_raw_data["Data"] = group_metrics(metrics_dict, "County")
                    else:
                        metrics_list = []
                        for metrics_key, metrics_entry in metrics_dict.iteritems():
                            metrics_list.append(metrics_entry)
                        response_raw_data["Data"] = metrics_list
                        response_raw_data["Data"] = metrics_dict
                else:
                    metrics_list = []
                    for metrics_key, metrics_entry in metrics_dict.iteritems():
                        metrics_list.append(metrics_entry)
                    response_raw_data["Data"] = metrics_list
                    # response_raw_data["Data"] = metrics_dict
            else:
                response_raw_data['Status']['Error Code'] = 1
                rqst_errors.append('No metrics entries found in database')
        else:
            list_of_ids = re.findall("\d+", rqst_staff_id)
            if len(list_of_ids) > 0:
                for indx, element in enumerate(list_of_ids):
                    list_of_ids[indx] = int(element)
                if list_of_counties is not None:
                    metrics_submissions = []
                    for county in list_of_counties:
                        county_metrics = MetricsSubmission.objects.filter(county__iexact=county, staff_member__in=list_of_ids)
                        for metrics_entry in county_metrics:
                            metrics_submissions.append(metrics_entry)
                else:
                    metrics_submissions = MetricsSubmission.objects.filter(staff_member__in=list_of_ids)

                if len(metrics_submissions) > 0:
                    metrics_dict = {}
                    for metrics_submission in metrics_submissions:
                        if metrics_submission.staff_member_id not in metrics_dict:
                            metrics_dict[metrics_submission.staff_member_id] = {"Metrics Data": [metrics_submission.return_values_dict()]}
                            metrics_dict[metrics_submission.staff_member_id]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                        else:
                            metrics_dict[metrics_submission.staff_member_id]["Metrics Data"].append(
                                    metrics_submission.return_values_dict())
                    if "groupby" in rqst_params:
                        if rqst_params["groupby"] == "county" or rqst_params["groupby"] == "County":
                            metrics_dict = group_metrics(metrics_dict, "County")
                            metrics_list = []
                            for metrics_key, metrics_entry in metrics_dict.iteritems():
                                metrics_list.append(metrics_entry)
                            response_raw_data["Data"] = metrics_list
                            # response_raw_data["Data"] = group_metrics(metrics_dict, "County")
                        else:
                            metrics_list = []
                            for metrics_key, metrics_entry in metrics_dict.iteritems():
                                metrics_list.append(metrics_entry)
                            response_raw_data["Data"] = metrics_list
                            # response_raw_data["Data"] = metrics_dict
                    else:
                        metrics_list = []
                        for metrics_key, metrics_entry in metrics_dict.iteritems():
                            metrics_list.append(metrics_entry)
                        response_raw_data["Data"] = metrics_list
                        # response_raw_data["Data"] = metrics_dict

                    for staff_id in list_of_ids:
                        if staff_id not in metrics_dict:
                            if response_raw_data['Status']['Error Code'] != 2:
                                response_raw_data['Status']['Error Code'] = 2
                            rqst_errors.append('Metrics for staff Member with id: {!s} not found in database'.format(str(staff_id)))
                else:
                    response_raw_data['Status']['Error Code'] = 1
                    rqst_errors.append('No metrics entries for staff ID(s): {!s} not found in database'.format(rqst_staff_id))
            else:
                response_raw_data['Status']['Error Code'] = 1
                rqst_errors.append('No staff IDs provided in request')

    elif 'fname' in rqst_params and 'lname' in rqst_params:
        list_of_first_names = re.findall("[\w. '-]+", rqst_params['fname'])
        list_of_last_names = re.findall("[\w. '-]+", rqst_params['lname'])

        if len(list_of_first_names) == len(list_of_last_names):
            list_of_ids = []
            for i, first_name in enumerate(list_of_first_names):
                last_name = list_of_last_names[i]
                name_ids = PICStaff.objects.filter(first_name__iexact=first_name, last_name__iexact=last_name).values_list('id', flat=True)
                if len(name_ids) > 0:
                    list_of_ids.append(name_ids)
                else:
                    if response_raw_data['Status']['Error Code'] != 2:
                        response_raw_data['Status']['Error Code'] = 2
                    rqst_errors.append('Metrics for staff member with name: {!s} {!s} not found in database'.format(first_name, last_name))
            list_of_ids = list(set().union(*list_of_ids))
            if len(list_of_ids) > 0:
                for indx, element in enumerate(list_of_ids):
                    list_of_ids[indx] = int(element)
                if list_of_counties is not None:
                    metrics_submissions = []
                    for county in list_of_counties:
                        county_metrics = MetricsSubmission.objects.filter(county__iexact=county, staff_member__in=list_of_ids)
                        for metrics_entry in county_metrics:
                            metrics_submissions.append(metrics_entry)
                else:
                    metrics_submissions = MetricsSubmission.objects.filter(staff_member__in=list_of_ids)

                if len(metrics_submissions) > 0:
                    metrics_dict = {}
                    for metrics_submission in metrics_submissions:
                        name = '{!s} {!s}'.format(metrics_submission.staff_member.first_name, metrics_submission.staff_member.last_name)
                        if name not in metrics_dict:
                            metrics_dict[name] = {"Metrics Data": [metrics_submission.return_values_dict()]}
                            metrics_dict[name]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                        else:
                            metrics_dict[name]["Metrics Data"].append(metrics_submission.return_values_dict())
                    if "groupby" in rqst_params:
                        if rqst_params["groupby"] == "county" or rqst_params["groupby"] == "County":
                            metrics_dict = group_metrics(metrics_dict, "County")
                            metrics_list = []
                            for metrics_key, metrics_entry in metrics_dict.iteritems():
                                metrics_list.append(metrics_entry)
                            response_raw_data["Data"] = metrics_list
                            # response_raw_data["Data"] = group_metrics(metrics_dict, "County")
                        else:
                            metrics_list = []
                            for metrics_key, metrics_entry in metrics_dict.iteritems():
                                metrics_list.append(metrics_entry)
                            response_raw_data["Data"] = metrics_list
                            # response_raw_data["Data"] = metrics_dict
                    else:
                        metrics_list = []
                        for metrics_key, metrics_entry in metrics_dict.iteritems():
                            metrics_list.append(metrics_entry)
                        response_raw_data["Data"] = metrics_list
                        # response_raw_data["Data"] = metrics_dict

                else:
                    if response_raw_data['Status']['Error Code'] != 2:
                        rqst_errors.append('No metrics entries for first: {!s} and last name(s): {!s} not found in database'.format(rqst_params['fname'],
                                                                                                                                    rqst_params['lname']))
                    response_raw_data['Status']['Error Code'] = 1
            else:
                if response_raw_data['Status']['Error Code'] != 2:
                    rqst_errors.append('No staff entries for first: {!s} and last name(s): {!s} not found in database'.format(rqst_params['fname'],
                                                                                                                              rqst_params['lname']))
                response_raw_data['Status']['Error Code'] = 1
        else:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('Length of first name list must be equal to length of last name list')

    elif 'email' in rqst_params:
        list_of_emails = re.findall(r"[\w. '-@]+", rqst_params['email'])
        # response_raw_data['Data'] = list_of_emails
        list_of_ids = []
        for email in list_of_emails:
            email_ids = PICStaff.objects.filter(email__iexact=email).values_list('id', flat=True)
            if len(email_ids) > 0:
                list_of_ids.append(email_ids)
            else:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Staff member with email: {!s} not found in database'.format(email))
        list_of_ids = list(set().union(*list_of_ids))
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            if list_of_counties is not None:
                metrics_submissions = []
                for county in list_of_counties:
                    county_metrics = MetricsSubmission.objects.filter(county__iexact=county, staff_member__in=list_of_ids)
                    for metrics_entry in county_metrics:
                        metrics_submissions.append(metrics_entry)
            else:
                metrics_submissions = MetricsSubmission.objects.filter(staff_member__in=list_of_ids)

            if len(metrics_submissions) > 0:
                metrics_dict = {}
                for metrics_submission in metrics_submissions:
                    if metrics_submission.staff_member.email not in metrics_dict:
                        metrics_dict[metrics_submission.staff_member.email] = {"Metrics Data": [metrics_submission.return_values_dict()]}
                        metrics_dict[metrics_submission.staff_member.email]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                    else:
                        metrics_dict[metrics_submission.staff_member.email]["Metrics Data"].append(metrics_submission.return_values_dict())
                if "groupby" in rqst_params:
                    if rqst_params["groupby"] == "county" or rqst_params["groupby"] == "County":
                        metrics_dict = group_metrics(metrics_dict, "County")
                        metrics_list = []
                        for metrics_key, metrics_entry in metrics_dict.iteritems():
                            metrics_list.append(metrics_entry)
                        response_raw_data["Data"] = metrics_list
                        # response_raw_data["Data"] = group_metrics(metrics_dict, "County")
                    else:
                        metrics_list = []
                        for metrics_key, metrics_entry in metrics_dict.iteritems():
                            metrics_list.append(metrics_entry)
                        response_raw_data["Data"] = metrics_list
                        # response_raw_data["Data"] = metrics_dict
                else:
                    metrics_list = []
                    for metrics_key, metrics_entry in metrics_dict.iteritems():
                        metrics_list.append(metrics_entry)
                    response_raw_data["Data"] = metrics_list
                    # response_raw_data["Data"] = metrics_dict

            else:
                if response_raw_data['Status']['Error Code'] != 2:
                    rqst_errors.append('No metrics entries for email(s): {!s} not found in database'.format(rqst_params['email']))
                response_raw_data['Status']['Error Code'] = 1
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for email(s): {!s} not found in database'.format(rqst_params['email']))
            response_raw_data['Status']['Error Code'] = 1

    elif 'fname' in rqst_params:
        list_of_first_names = re.findall("[\w. '-]+", rqst_params['fname'])
        list_of_ids = []
        for first_name in list_of_first_names:
            first_name_ids = PICStaff.objects.filter(first_name__iexact=first_name).values_list('id', flat=True)
            if len(first_name_ids) > 0:
                list_of_ids.append(first_name_ids)
            else:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Metrics for staff member with first name: {!s} not found in database'.format(first_name))
        list_of_ids = list(set().union(*list_of_ids))
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            if list_of_counties is not None:
                metrics_submissions = []
                for county in list_of_counties:
                    county_metrics = MetricsSubmission.objects.filter(county__iexact=county, staff_member__in=list_of_ids)
                    for metrics_entry in county_metrics:
                        metrics_submissions.append(metrics_entry)
            else:
                metrics_submissions = MetricsSubmission.objects.filter(staff_member__in=list_of_ids)

            if len(metrics_submissions) > 0:
                metrics_dict = {}
                for metrics_submission in metrics_submissions:
                    if metrics_submission.staff_member.first_name not in metrics_dict:
                        metrics_dict[metrics_submission.staff_member.first_name] = {"Metrics Data": [metrics_submission.return_values_dict()]}
                        metrics_dict[metrics_submission.staff_member.first_name]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                    else:
                        metrics_dict[metrics_submission.staff_member.first_name]["Metrics Data"].append(metrics_submission.return_values_dict())
                if "groupby" in rqst_params:
                    if rqst_params["groupby"] == "county" or rqst_params["groupby"] == "County":
                        metrics_dict = group_metrics(metrics_dict, "County")
                        metrics_list = []
                        for metrics_key, metrics_entry in metrics_dict.iteritems():
                            metrics_list.append(metrics_entry)
                        response_raw_data["Data"] = metrics_list
                        # response_raw_data["Data"] = group_metrics(metrics_dict, "County")
                    else:
                        metrics_list = []
                        for metrics_key, metrics_entry in metrics_dict.iteritems():
                            metrics_list.append(metrics_entry)
                        response_raw_data["Data"] = metrics_list
                        # response_raw_data["Data"] = metrics_dict
                else:
                    metrics_list = []
                    for metrics_key, metrics_entry in metrics_dict.iteritems():
                        metrics_list.append(metrics_entry)
                    response_raw_data["Data"] = metrics_list
                    # response_raw_data["Data"] = metrics_dict

            else:
                if response_raw_data['Status']['Error Code'] != 2:
                    rqst_errors.append('No metrics entries for first name(s): {!s} not found in database'.format(rqst_params['fname']))
                response_raw_data['Status']['Error Code'] = 1
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for first name(s): {!s} not found in database'.format(rqst_params['fname']))
            response_raw_data['Status']['Error Code'] = 1

    elif 'lname' in rqst_params:
        list_of_last_names = re.findall("[\w. '-]+", rqst_params['lname'])
        list_of_ids = []
        for last_name in list_of_last_names:
            last_name_ids = PICStaff.objects.filter(last_name__iexact=last_name).values_list('id', flat=True)
            if len(last_name_ids) > 0:
                list_of_ids.append(last_name_ids)
            else:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Metrics for staff member with last name: {!s} not found in database'.format(last_name))
        list_of_ids = list(set().union(*list_of_ids))
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            if list_of_counties is not None:
                metrics_submissions = []
                for county in list_of_counties:
                    county_metrics = MetricsSubmission.objects.filter(county__iexact=county, staff_member__in=list_of_ids)
                    for metrics_entry in county_metrics:
                        metrics_submissions.append(metrics_entry)
            else:
                metrics_submissions = MetricsSubmission.objects.filter(staff_member__in=list_of_ids)

            if len(metrics_submissions) > 0:
                metrics_dict = {}
                for metrics_submission in metrics_submissions:
                    if metrics_submission.staff_member.last_name not in metrics_dict:
                        metrics_dict[metrics_submission.staff_member.last_name] = {"Metrics Data": [metrics_submission.return_values_dict()]}
                        metrics_dict[metrics_submission.staff_member.last_name]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                    else:
                        metrics_dict[metrics_submission.staff_member.last_name]["Metrics Data"].append(metrics_submission.return_values_dict())
                if "groupby" in rqst_params:
                    if rqst_params["groupby"] == "county" or rqst_params["groupby"] == "County":
                        metrics_dict = group_metrics(metrics_dict, "County")
                        metrics_list = []
                        for metrics_key, metrics_entry in metrics_dict.iteritems():
                            metrics_list.append(metrics_entry)
                        response_raw_data["Data"] = metrics_list
                        # response_raw_data["Data"] = group_metrics(metrics_dict, "County")
                    else:
                        metrics_list = []
                        for metrics_key, metrics_entry in metrics_dict.iteritems():
                            metrics_list.append(metrics_entry)
                        response_raw_data["Data"] = metrics_list
                        # response_raw_data["Data"] = metrics_dict
                else:
                    metrics_list = []
                    for metrics_key, metrics_entry in metrics_dict.iteritems():
                        metrics_list.append(metrics_entry)
                    response_raw_data["Data"] = metrics_list
                    # response_raw_data["Data"] = metrics_dict

            else:
                if response_raw_data['Status']['Error Code'] != 2:
                    rqst_errors.append('No metrics entries for last name(s): {!s} not found in database'.format(rqst_params['lname']))
                response_raw_data['Status']['Error Code'] = 1
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for last name(s): {!s} not found in database'.format(rqst_params['lname']))
            response_raw_data['Status']['Error Code'] = 1

    elif list_of_counties is not None:
        metrics_submissions = []
        for county in list_of_counties:
            county_metrics = MetricsSubmission.objects.filter(county__iexact=county)
            for metrics_entry in county_metrics:
                metrics_submissions.append(metrics_entry)

        if len(metrics_submissions) > 0:
            metrics_dict = {}
            for metrics_submission in metrics_submissions:
                if metrics_submission.staff_member_id not in metrics_dict:
                    metrics_dict[metrics_submission.staff_member_id] = {"Metrics Data": [metrics_submission.return_values_dict()]}
                    metrics_dict[metrics_submission.staff_member_id]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                else:
                    metrics_dict[metrics_submission.staff_member_id]["Metrics Data"].append(metrics_submission.return_values_dict())
            if "groupby" in rqst_params:
                if rqst_params["groupby"] == "county" or rqst_params["groupby"] == "County":
                    metrics_dict = group_metrics(metrics_dict, "County")
                    metrics_list = []
                    for metrics_key, metrics_entry in metrics_dict.iteritems():
                        metrics_list.append(metrics_entry)
                    response_raw_data["Data"] = metrics_list
                    # response_raw_data["Data"] = group_metrics(metrics_dict, "County")
                else:
                    metrics_list = []
                    for metrics_key, metrics_entry in metrics_dict.iteritems():
                        metrics_list.append(metrics_entry)
                    response_raw_data["Data"] = metrics_list
                    # response_raw_data["Data"] = metrics_dict
            else:
                metrics_list = []
                for metrics_key, metrics_entry in metrics_dict.iteritems():
                    metrics_list.append(metrics_entry)
                response_raw_data["Data"] = metrics_list
                # response_raw_data["Data"] = metrics_dict

        else:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('No metrics entries found in database for counties: {!s}'.format(rqst_counties))
    else:
        response_raw_data['Status']['Error Code'] = 1
        rqst_errors.append('No Params')

    response_raw_data["Status"]["Errors"] = rqst_errors
    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response
