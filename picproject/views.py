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
from picmodels.models import PICUser, PICAppointment, Appointment, Location, PICConsumer, PICStaff, MetricsSubmission
import datetime, json
from django.views.decorators.csrf import csrf_exempt
import sys


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


def clean_json_string_input(json_dict, dict_name, dict_key, post_errors):
    if dict_key not in json_dict:
        post_errors.append("\"" + dict_key + "\" key not found in " + dict_name + " dictionary")
    elif json_dict[dict_key] == "":
        post_errors.append("Value for \"" + dict_key + "\" in " + dict_name + " dict is an empty string")
    elif json_dict[dict_key] is None:
        post_errors.append("Value for \"" + dict_key + "\" in " + dict_name + " dict is Null")
    else:
        return str(json_dict[dict_key])
    return None


def clean_json_int_input(json_dict, dict_name, dict_key, post_errors):
    if dict_key not in json_dict:
        post_errors.append("\"" + dict_key + "\" key not found in " + dict_name + " dictionary")
    elif json_dict[dict_key] is None:
        post_errors.append("Value for \"" + dict_key + "\" in " + dict_name + " dict is Null")
    else:
        return int(json_dict[dict_key])
    return None


# defines view for saving scheduled appointments to the database
@csrf_exempt
def appointment_submission_handler(request):
    #initialize dictionary for response data, including parsing errors
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

        if "Preferred Language" not in post_json:
            post_errors.append("\"Preferred Language\" key not found in root dictionary")
        elif post_json["Preferred Language"] is None:
            post_errors.append("Value for \"Preferred Language\" is Null")
        else:
            request_consumer_preferred_language = str(post_json["Preferred Language"])

        if "Best Contact Time" not in post_json:
            post_errors.append("\"Best Contact Time\" key not found in root dictionary")
        elif post_json["Best Contact Time"] is None:
            post_errors.append("Value for \"Best Contact Time\" is Null")
        else:
            request_consumer_best_contact_time = str(post_json["Best Contact Time"])

        if "Appointment" not in post_json:
            post_errors.append("\"Appointment\" key not found in root dictionary")
        elif post_json["Appointment"] is None:
            post_errors.append("Value for \"Appointment\" is Null")
        elif post_json["Appointment"] == {}:
            post_errors.append("Value for \"Appointment\" is an empty dictionary")
        else:
            appointment_information = post_json["Appointment"]
            request_location_name = clean_json_string_input(appointment_information, "Appointment Information", "Name", post_errors)
            request_appointment_address = clean_json_string_input(appointment_information, "Appointment Information", "Street Address", post_errors)
            request_appointment_address = request_appointment_address + ", " + clean_json_string_input(appointment_information,  "Appointment Information", "City", post_errors)
            request_appointment_address = request_appointment_address + " " + clean_json_string_input(appointment_information, "Appointment Information", "State", post_errors)
            request_appointment_address = request_appointment_address + ", " + clean_json_string_input(appointment_information, "Appointment Information", "Zip Code", post_errors)
            request_appointment_location_phone = clean_json_string_input(appointment_information, "Appointment Information", "Phone Number", post_errors)

            if "Appointment Slot" not in appointment_information:
                post_errors.append("\"Appointment Slot\" key not found in 'Appointment Information' dictionary")
            elif appointment_information["Appointment Slot"] is None:
                post_errors.append("Value for \"Appointment Slot\" in 'Appointment Information' dict is Null")
            elif appointment_information["Appointment Slot"] == {}:
                post_errors.append("Value for \"Appointment Slot\" in 'Appointment Information' dict is an empty dict")
            else:
                appointment_slot_info = appointment_information["Appointment Slot"]

                if "Date" not in appointment_slot_info:
                    post_errors.append("\"Date\" key not found in \"Appointment Slot\" dictionary")
                elif appointment_slot_info["Date"] == {}:
                    post_errors.append("Value for \"Date\" in \"Appointment Slot\" dict is an empty dictionary")
                elif appointment_slot_info["Date"] is None:
                    post_errors.append("Value for \"Date\" in \"Appointment Slot\" dict is Null")
                else:
                    datedict = appointment_slot_info["Date"]
                    month = clean_json_int_input(datedict, "Date", "Month", post_errors)
                    day = clean_json_int_input(datedict, "Date", "Day", post_errors)
                    year = clean_json_int_input(datedict, "Date", "Year", post_errors)

                    datetuple = (year, month, day)
                    if None not in datetuple:
                        apt_date = datetime.date(datetuple[0], datetuple[1], datetuple[2]).isoformat()
                        request_appointment_date = str(apt_date)

                if "Start Time" not in appointment_slot_info:
                    post_errors.append("\"Start Time\" key not found in \"Appointment Slot\" dictionary")
                elif appointment_slot_info["Start Time"] == {}:
                    post_errors.append("Value for \"Start Time\" in \"Appointment Slot\" dict is an empty dictionary")
                elif appointment_slot_info["Start Time"] is None:
                    post_errors.append("Value for \"Start Time\" in \"Appointment Slot\" dict is Null")
                else:
                    starttimedict = appointment_slot_info["Start Time"]
                    hour = clean_json_int_input(starttimedict, "Start Time", "Hour", post_errors)
                    minutes = clean_json_int_input(starttimedict, "Start Time", "Minutes", post_errors)

                    if hour is not None and minutes is not None:
                        request_appointment_start_time = str(datetime.time(hour=hour, minute=minutes).isoformat())

                if "End Time" not in appointment_slot_info:
                    post_errors.append("\"End Time\" key not found in \"Appointment Slot\" dictionary")
                elif appointment_slot_info["End Time"] == {}:
                    post_errors.append("Value for \"End Time\" in \"Appointment Slot\" dict is an empty dictionary")
                elif appointment_slot_info["End Time"] is None:
                    post_errors.append("Value for \"End Time\" in \"Appointment Slot\" dict is Null")
                else:
                    endtimedict = appointment_slot_info["End Time"]
                    hour = clean_json_int_input(endtimedict, "End Time", "Hour", post_errors)
                    minutes = clean_json_int_input(endtimedict, "End Time", "Minutes", post_errors)

                    if hour is not None and minutes is not None:
                        request_appointment_end_time = str(datetime.time(hour=hour, minute=minutes).isoformat())

            if "Point of Contact" not in appointment_information:
                post_errors.append("\"Point of Contact\" key not found in 'Appointment Information' dictionary")
            elif appointment_information["Point of Contact"] is None:
                post_errors.append("Value for \"Point of Contact\" in 'Appointment Information' dict is Null")
            elif appointment_information["Point of Contact"] == {}:
                post_errors.append("Value for \"Point of Contact\" in 'Appointment Information' dict is an empty dict")
            else:
                appointment_poc_info = appointment_information["Point of Contact"]
                request_poc_first_name = clean_json_string_input(appointment_poc_info, "Point of Contact", "First Name", post_errors)
                request_poc_last_name = clean_json_string_input(appointment_poc_info, "Point of Contact", "Last Name", post_errors)
                request_poc_email = clean_json_string_input(appointment_poc_info, "Point of Contact", "Email", post_errors)
                request_poc_type = clean_json_string_input(appointment_poc_info, "Point of Contact", "Type", post_errors)

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

            for message in post_errors:
                print message
                sys.stdout.flush()

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
def metrics_submission_handler(request):
    #initialize dictionary for response data, including parsing errors
    response_raw_data = {'status': {"Error Code": 0, "Version": 1.0}}
    post_errors = []

    if request.method == 'POST' or request.is_ajax():
        post_data = request.body
        post_json = json.loads(post_data)

        #Code to parse POSTed json request
        rqst_usr_email = clean_json_string_input(post_json, "root", "Email", post_errors)
        rqst_usr_f_name = clean_json_string_input(post_json, "root", "First Name", post_errors)
        rqst_usr_l_name = clean_json_string_input(post_json, "root", "Last Name", post_errors)
        rqst_usr_type = clean_json_string_input(post_json, "root", "User Type", post_errors)

        if "Consumer Metrics"  not in post_json:
            post_errors.append("\"Consumer Metrics\" key not found in root dictionary")
        elif post_json["Consumer Metrics"] is None:
            post_errors.append("Value for \"Consumer Metrics\" is Null")
        elif post_json["Consumer Metrics"] == {}:
            post_errors.append("Value for \"Consumer Metrics\" is an empty dictionary")
        else:
            consumer_metrics = post_json["Consumer Metrics"]

            rqst_cons_rec_edu = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Received Education", post_errors)
            rqst_cons_app_maid = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Applied Medicaid", post_errors)
            rqst_cons_sel_qhp = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Selected QHP", post_errors)
            rqst_cons_enr_shop = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Enrolled SHOP", post_errors)
            rqst_cons_ref_maidorchip = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Referred Medicaid or CHIP", post_errors)
            rqst_cons_ref_shop = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Referred SHOP", post_errors)
            rqst_cons_filed_exemptions = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Filed Exemptions", post_errors)
            rqst_cons_rec_postenr_support = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Received Post-Enrollment Support", post_errors)
            rqst_cons_trends = clean_json_string_input(consumer_metrics, "Consumer Metrics", "Trends", post_errors)
            rqst_cons_success_story = clean_json_string_input(consumer_metrics, "Consumer Metrics", "Success Story", post_errors)
            rqst_cons_hard_or_diff = clean_json_string_input(consumer_metrics, "Consumer Metrics", "Hardship or Difficulty", post_errors)

            if "Comments" not in consumer_metrics:
                post_errors.append("\"Comments\" key not found in \"Consumer Metrics\" dictionary")
            else:
                rqst_usr_comments = str(consumer_metrics["Comments"])

            if "Outreach and Stakeholder Activities" not in consumer_metrics:
                post_errors.append("\"Outreach and Stakeholder Activities\" key not found in \"Consumer Metrics\" dictionary")
            else:
                rqst_usr_outr_stkehol_act = str(consumer_metrics["Outreach and Stakeholder Activities"])

            if rqst_usr_type == "IPC":
                rqst_cons_apts_sched = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Appointments Scheduled", post_errors)
                rqst_cons_confirm_calls = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Confirmation Calls", post_errors)
                rqst_cons_apts_held = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Appointments Held", post_errors)
                rqst_cons_apts_over_hour = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Appointments Over Hour", post_errors)
                rqst_cons_apts_cplx_market = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Appointments Complex Market", post_errors)
                rqst_cons_apts_cplx_maid = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Appointments Complex Medicaid", post_errors)
                rqst_cons_apts_postenr_assis = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Appointments Post-Enrollment Assistance", post_errors)
                rqst_cons_apts_over_3_hours = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Appointments Over 3 Hours", post_errors)

        # if there are no parsing errors, get or create database entries for consumer, location, and point of contact
        # create and save database entry for appointment
        if len(post_errors) == 0:
            usr_rqst_values = {"first_name": rqst_usr_f_name,
                               "last_name": rqst_usr_l_name,
                               "type": rqst_usr_type}
            user_instance, user_instance_created = PICStaff.objects.get_or_create(email=rqst_usr_email,
                                                                                  defaults=usr_rqst_values)

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
                                                     outreach_stakeholder_activity=rqst_usr_outr_stkehol_act)

            if rqst_usr_type == "IPC":
                new_metrics_instance.appointments_scheduled = rqst_cons_apts_sched
                new_metrics_instance.confirmation_calls = rqst_cons_confirm_calls
                new_metrics_instance.appointments_held = rqst_cons_apts_held
                new_metrics_instance.appointments_over_hour = rqst_cons_apts_over_hour
                new_metrics_instance.appointments_over_three_hours = rqst_cons_apts_over_3_hours
                new_metrics_instance.appointments_cmplx_market = rqst_cons_apts_cplx_market
                new_metrics_instance.appointments_cmplx_medicaid = rqst_cons_apts_cplx_maid
                new_metrics_instance.appointments_postenroll_assistance =rqst_cons_apts_postenr_assis

            new_metrics_instance.save()

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
