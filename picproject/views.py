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
        #Code to parse POSTed json request
        if "Email" not in post_json:
            post_errors.append("\"Email\" key not found in root dictionary")
        elif post_json["Email"] == "":
            post_errors.append("Value for \"Email\" is an empty string")
        elif post_json["Email"] is None:
            post_errors.append("Value for \"Email\" is Null")
        else:
            request_consumer_email = str(post_json["Email"])

        if "First Name" not in post_json:
            post_errors.append("\"First Name\" key not found in root dictionary")
        elif post_json["First Name"] == "":
            post_errors.append("Value for \"First Name\" is an empty string")
        elif post_json["First Name"] is None:
            post_errors.append("Value for \"First Name\" is Null")
        else:
            request_consumer_first_name = str(post_json["First Name"])

        if "Last Name" not in post_json:
            post_errors.append("\"Last Name\" key not found in root dictionary")
        elif post_json["Last Name"] == "":
            post_errors.append("Value for \"Last Name\" is an empty string")
        elif post_json["Last Name"] is None:
            post_errors.append("Value for \"Last Name\" is Null")
        else:
            request_consumer_last_name = str(post_json["Last Name"])

        if "Phone Number" not in post_json:
            post_errors.append("\"Phone Number\" key not found in root dictionary")
        elif post_json["Phone Number"] == "":
            post_errors.append("Value for \"Phone Number\" is an empty string")
        elif post_json["Phone Number"] is None:
            post_errors.append("Value for \"Phone Number\" is Null")
        else:
            request_consumer_phone = str(post_json["Phone Number"])

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

            if "Name" not in appointment_information:
                post_errors.append("\"Name\" key not found in \"Appointment Information\" dictionary")
            elif appointment_information["Name"] == "":
                post_errors.append("Value for \"Name\" in \"Appointment Information\" dict is an empty string")
            elif appointment_information["Name"] is None:
                post_errors.append("Value for \"Name\" in \"Appointment Information\" dict is Null")
            else:
                request_location_name = str(appointment_information["Name"])

            request_appointment_address = ""

            if "Street Address" not in appointment_information:
                post_errors.append("\"Street Address\" key not found in \"Appointment Information\" dictionary")
            elif appointment_information["Street Address"] == "":
                post_errors.append("Value for \"Street Address\" in \"Appointment Information\" dict is an empty string")
            elif appointment_information["Street Address"] is None:
                post_errors.append("Value for \"Street Address\" in \"Appointment Information\" dict is Null")
            else:
                request_appointment_address = str(appointment_information["Street Address"])

            if "City" not in appointment_information:
                post_errors.append("\"City\" key not found in \"Appointment Information\" dictionary")
            elif appointment_information["City"] == "":
                post_errors.append("Value for \"City\" in \"Appointment Information\" dict is an empty string")
            elif appointment_information["City"] is None:
                post_errors.append("Value for \"City\" in \"Appointment Information\" dict is Null")
            else:
                request_appointment_address = request_appointment_address + ", " + str(appointment_information["City"])

            if "State" not in appointment_information:
                post_errors.append("\"State\" key not found in \"Appointment Information\" dictionary")
            elif appointment_information["State"] == "":
                post_errors.append("Value for \"State\" in \"Appointment Information\" dict is an empty string")
            elif appointment_information["State"] is None:
                post_errors.append("Value for \"State\" in \"Appointment Information\" dict is Null")
            else:
                request_appointment_address = request_appointment_address + " " + str(appointment_information["State"])

            if "Zip Code" not in appointment_information:
                post_errors.append("\"Zip Code\" key not found in \"Appointment Information\" dictionary")
            elif appointment_information["Zip Code"] == "":
                post_errors.append("Value for \"Zip Code\" in \"Appointment Information\" dict is an empty string")
            elif appointment_information["Zip Code"] is None:
                post_errors.append("Value for \"Zip Code\" in \"Appointment Information\" dict is Null")
            else:
                request_appointment_address = request_appointment_address + ", " + str(appointment_information["Zip Code"])

            if "Phone Number" not in appointment_information:
                post_errors.append("\"Phone Number\" key not found in \"Appointment Information\" dictionary")
            elif appointment_information["Phone Number"] == "":
                post_errors.append("Value for \"Phone Number\" in \"Appointment Information\" dict is an empty string")
            elif appointment_information["Phone Number"] is None:
                post_errors.append("Value for \"Phone Number\" in \"Appointment Information\" dict is Null")
            else:
                request_appointment_location_phone = str(appointment_information["Phone Number"])

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
                    month = day = year = None
                    if "Month" not in datedict:
                        post_errors.append("\"Month\" key not found in \"Date\" dictionary")
                    if datedict["Month"] is None:
                        post_errors.append("Value for \"Month\" in \"Date\" dictionary is Null")
                    else:
                        month = int(datedict["Month"])

                    if "Day" not in datedict:
                        post_errors.append("\"Day\" key not found in \"Date\" dictionary")
                    if datedict["Day"] is None:
                        post_errors.append("Value for \"Day\" in \"Date\" dictionary is Null")
                    else:
                        day = int(datedict["Day"])

                    if "Year" not in datedict:
                        post_errors.append("\"Year\" key not found in \"Date\" dictionary")
                    if datedict["Year"] is None:
                        post_errors.append("Value for \"Year\" in \"Date\" dictionary is Null")
                    else:
                        year = int(datedict["Year"])

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
                    hour = minutes = None

                    if "Hour" not in starttimedict:
                        post_errors.append("\"Hour\" key not found in \"Start Time\" dictionary")
                    if starttimedict["Hour"] is None:
                        post_errors.append("Value for \"Hour\" in \"Start Time\" dictionary is Null")
                    else:
                        hour = int(starttimedict["Hour"])

                    if "Minutes" not in starttimedict:
                        post_errors.append("\"Minutes\" key not found in \"Start Time\" dictionary")
                    if starttimedict["Minutes"] is None:
                        post_errors.append("Value for \"Minutes\" in \"Start Time\" dictionary is Null")
                    else:
                        minutes = int(starttimedict["Minutes"])

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
                    hour = minutes = None

                    if "Hour" not in endtimedict:
                        post_errors.append("\"Hour\" key not found in \"End Time\" dictionary")
                    if endtimedict["Hour"] is None:
                        post_errors.append("Value for \"Hour\" in \"End Time\" dictionary is Null")
                    else:
                        hour = int(endtimedict["Hour"])

                    if "Minutes" not in endtimedict:
                        post_errors.append("\"Minutes\" key not found in \"End Time\" dictionary")
                    if endtimedict["Minutes"] is None:
                        post_errors.append("Value for \"Minutes\" in \"End Time\" dictionary is Null")
                    else:
                        minutes = int(endtimedict["Minutes"])

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

                if "First Name" not in appointment_poc_info:
                    post_errors.append("\"First Name\" key not found in \"Point of Contact\" dictionary")
                elif appointment_poc_info["First Name"] == "":
                    post_errors.append("Value for \"First Name\" in \"Point of Contact\" dict is an empty string")
                elif appointment_poc_info["First Name"] is None:
                    post_errors.append("Value for \"First Name\" in \"Point of Contact\" dict is Null")
                else:
                    request_poc_first_name = str(appointment_poc_info["First Name"])

                if "Last Name" not in appointment_poc_info:
                    post_errors.append("\"Last Name\" key not found in \"Point of Contact\" dictionary")
                elif appointment_poc_info["Last Name"] == "":
                    post_errors.append("Value for \"Last Name\" in \"Point of Contact\" dict is an empty string")
                elif appointment_poc_info["Last Name"] is None:
                    post_errors.append("Value for \"Last Name\" in \"Point of Contact\" dict is Null")
                else:
                    request_poc_last_name = str(appointment_poc_info["First Name"])

                if "Email" not in appointment_poc_info:
                    post_errors.append("\"Email\" key not found in \"Point of Contact\" dictionary")
                elif appointment_poc_info["Email"] == "":
                    post_errors.append("Value for \"Email\" in \"Point of Contact\" dict is an empty string")
                elif appointment_poc_info["Email"] is None:
                    post_errors.append("Value for \"Email\" in \"Point of Contact\" dict is Null")
                else:
                    request_poc_email = str(appointment_poc_info["Email"])

                if "Type" not in appointment_poc_info:
                    post_errors.append("\"Type\" key not found in \"Point of Contact\" dictionary")
                elif appointment_poc_info["Type"] == "":
                    post_errors.append("Value for \"Type\" in \"Point of Contact\" dict is an empty string")
                elif appointment_poc_info["Type"] is None:
                    post_errors.append("Value for \"Type\" in \"Point of Contact\" dict is Null")
                else:
                    request_poc_type = str(appointment_poc_info["Type"])

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

        # add parsing errors to response dictionary
        else:
            response_raw_data["status"]["Error Code"] = 1
            response_raw_data["status"]["Errors"] = post_errors

            for message in post_errors:
                print message
                sys.stdout.flush()

        response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
        response['Access-Control-Allow-Origin'] = "*"
        return response

    elif request.method == "OPTIONS":
        response = HttpResponse("")
        response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Methods'] = "POST, OPTIONS, GET"
        response['Access-Control-Allow-Headers'] = "X-Requested-With"
        response['Access-Control-Max-Age'] = "1800"
        return response

    # if a GET request is made, add error message to response data
    else:
        response_raw_data["status"]["Error Code"] = 1
        post_errors.append("Request needs POST data")
        response_raw_data["status"]["Errors"] = post_errors
        for message in post_errors:
            print message
            sys.stdout.flush()

        response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
        response['Access-Control-Allow-Origin'] = "*"
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
        if "Email" not in post_json:
            post_errors.append("\"Email\" key not found in root dictionary")
        elif post_json["Email"] == "":
            post_errors.append("Value for \"Email\" is an empty string")
        elif post_json["Email"] is None:
            post_errors.append("Value for \"Email\" is Null")
        else:
            rqst_usr_email = str(post_json["Email"])

        if "First Name" not in post_json:
            post_errors.append("\"First Name\" key not found in root dictionary")
        elif post_json["First Name"] == "":
            post_errors.append("Value for \"First Name\" is an empty string")
        elif post_json["First Name"] is None:
            post_errors.append("Value for \"First Name\" is Null")
        else:
            rqst_usr_f_name = str(post_json["First Name"])

        if "Last Name" not in post_json:
            post_errors.append("\"Last Name\" key not found in root dictionary")
        elif post_json["Last Name"] == "":
            post_errors.append("Value for \"Last Name\" is an empty string")
        elif post_json["Last Name"] is None:
            post_errors.append("Value for \"Last Name\" is Null")
        else:
            rqst_usr_l_name = str(post_json["Last Name"])

        rqst_usr_type = None
        if "User Type" not in post_json:
            post_errors.append("\"User Type\" key not found in root dictionary")
        elif post_json["User Type"] == "":
            post_errors.append("Value for \"User Type\" is an empty string")
        elif post_json["User Type"] is None:
            post_errors.append("Value for \"User Type\" is Null")
        else:
            rqst_usr_type = str(post_json["User Type"])

        if "Consumer Metrics" not in post_json:
            post_errors.append("\"Consumer Metrics\" key not found in root dictionary")
        elif post_json["Consumer Metrics"] is None:
            post_errors.append("Value for \"Consumer Metrics\" is Null")
        elif post_json["Consumer Metrics"] == {}:
            post_errors.append("Value for \"Consumer Metrics\" is an empty dictionary")
        else:
            consumer_metrics = post_json["Consumer Metrics"]

            if "Received Education" not in consumer_metrics:
                post_errors.append("\"Received Education\" key not found in \"Consumer Metrics\" dictionary")
            elif consumer_metrics["Received Education"] is None:
                post_errors.append("Value for \"Received Education\" in \"Consumer Metrics\" dict is Null")
            else:
                rqst_cons_rec_edu = int(consumer_metrics["Received Education"])

            if "Applied Medicaid" not in consumer_metrics:
                post_errors.append("\"Applied Medicaid\" key not found in \"Consumer Metrics\" dictionary")
            elif consumer_metrics["Applied Medicaid"] is None:
                post_errors.append("Value for \"Applied Medicaid\" in \"Consumer Metrics\" dict is Null")
            else:
                rqst_cons_app_maid = int(consumer_metrics["Applied Medicaid"])

            if "Selected QHP" not in consumer_metrics:
                post_errors.append("\"Selected QHP\" key not found in \"Consumer Metrics\" dictionary")
            elif consumer_metrics["Selected QHP"] is None:
                post_errors.append("Value for \"Selected QHP\" in \"Consumer Metrics\" dict is Null")
            else:
                rqst_cons_sel_qhp = int(consumer_metrics["Selected QHP"])

            if "Enrolled SHOP" not in consumer_metrics:
                post_errors.append("\"Enrolled SHOP\" key not found in \"Consumer Metrics\" dictionary")
            elif consumer_metrics["Enrolled SHOP"] is None:
                post_errors.append("Value for \"Enrolled SHOP\" in \"Consumer Metrics\" dict is Null")
            else:
                rqst_cons_enr_shop = int(consumer_metrics["Enrolled SHOP"])

            if "Referred Medicaid or CHIP" not in consumer_metrics:
                post_errors.append("\"Referred Medicaid or CHIP\" key not found in \"Consumer Metrics\" dictionary")
            elif consumer_metrics["Referred Medicaid or CHIP"] is None:
                post_errors.append("Value for \"Referred Medicaid or CHIP\" in \"Consumer Metrics\" dict is Null")
            else:
                rqst_cons_ref_maidorchip = int(consumer_metrics["Referred Medicaid or CHIP"])

            if "Referred SHOP" not in consumer_metrics:
                post_errors.append("\"Referred SHOP\" key not found in \"Consumer Metrics\" dictionary")
            elif consumer_metrics["Referred SHOP"] is None:
                post_errors.append("Value for \"Referred Medicaid or SHOP\" in \"Consumer Metrics\" dict is Null")
            else:
                rqst_cons_ref_shop = int(consumer_metrics["Referred SHOP"])

            if "Filed Exemptions" not in consumer_metrics:
                post_errors.append("\"Filed Exemptions\" key not found in \"Consumer Metrics\" dictionary")
            elif consumer_metrics["Filed Exemptions"] is None:
                post_errors.append("Value for \"Filed Exemptions\" in \"Consumer Metrics\" dict is Null")
            else:
                rqst_cons_filed_exemptions = int(consumer_metrics["Filed Exemptions"])

            if "Received Post-Enrollment Support" not in consumer_metrics:
                post_errors.append("\"Received Post-Enrollment Support\" key not found in \"Consumer Metrics\" dictionary")
            elif consumer_metrics["Received Post-Enrollment Support"] is None:
                post_errors.append("Value for \"Received Post-Enrollment Support\" in \"Consumer Metrics\" dict is Null")
            else:
                rqst_cons_rec_postenr_support = int(consumer_metrics["Received Post-Enrollment Support"])

            if "Trends" not in consumer_metrics:
                post_errors.append("\"Trends\" key not found in \"Consumer Metrics\" dictionary")
            elif consumer_metrics["Trends"] == "":
                post_errors.append("Value for \"Trends\" in \"Consumer Metrics\" dict is an empty string")
            elif consumer_metrics["Trends"] is None:
                post_errors.append("Value for \"Trends\" in \"Consumer Metrics\" dict is Null")
            else:
                rqst_cons_trends = str(consumer_metrics["Trends"])

            if "Success Story" not in consumer_metrics:
                post_errors.append("\"Success Story\" key not found in \"Consumer Metrics\" dictionary")
            elif consumer_metrics["Success Story"] == "":
                post_errors.append("Value for \"Success Story\" in \"Consumer Metrics\" dict is an empty string")
            elif consumer_metrics["Success Story"] is None:
                post_errors.append("Value for \"Success Story\" in \"Consumer Metrics\" dict is Null")
            else:
                rqst_cons_success_story = str(consumer_metrics["Success Story"])

            if "Hardship or Difficulty" not in consumer_metrics:
                post_errors.append("\"Hardship or Difficulty\" key not found in \"Consumer Metrics\" dictionary")
            elif consumer_metrics["Hardship or Difficulty"] == "":
                post_errors.append("Value for \"Hardship or Difficulty\" in \"Consumer Metrics\" dict is an empty string")
            elif consumer_metrics["Hardship or Difficulty"] is None:
                post_errors.append("Value for \"Hardship or Difficulty\" in \"Consumer Metrics\" dict is Null")
            else:
                rqst_cons_hard_or_diff = str(consumer_metrics["Hardship or Difficulty"])

            if "Comments" not in consumer_metrics:
                post_errors.append("\"Comments\" key not found in \"Consumer Metrics\" dictionary")
            else:
                rqst_usr_comments = str(consumer_metrics["Comments"])

            if "Outreach and Stakeholder Activities" not in consumer_metrics:
                post_errors.append("\"Outreach and Stakeholder Activities\" key not found in \"Consumer Metrics\" dictionary")
            else:
                rqst_usr_outr_stkehol_act = str(consumer_metrics["Outreach and Stakeholder Activities"])

            if rqst_usr_type == "IPC":
                if "Appointments Scheduled" not in consumer_metrics:
                    post_errors.append("\"Appointments Scheduled\" key not found in \"Consumer Metrics\" dictionary")
                elif consumer_metrics["Appointments Scheduled"] is None:
                    post_errors.append("Value for \"Appointments Scheduled\" in \"Consumer Metrics\" dict is Null")
                else:
                    rqst_cons_apts_sched = int(consumer_metrics["Appointments Scheduled"])

                if "Confirmation Calls" not in consumer_metrics:
                    post_errors.append("\"Confirmation Calls\" key not found in \"Consumer Metrics\" dictionary")
                elif consumer_metrics["Confirmation Calls"] is None:
                    post_errors.append("Value for \"Confirmation Calls\" in \"Consumer Metrics\" dict is Null")
                else:
                    rqst_cons_confirm_calls = int(consumer_metrics["Confirmation Calls"])

                if "Appointments Held" not in consumer_metrics:
                    post_errors.append("\"Appointments Held\" key not found in \"Consumer Metrics\" dictionary")
                elif consumer_metrics["Appointments Held"] is None:
                    post_errors.append("Value for \"Appointments Held\" in \"Consumer Metrics\" dict is Null")
                else:
                    rqst_cons_apts_held = int(consumer_metrics["Appointments Held"])

                if "Appointments Over Hour" not in consumer_metrics:
                    post_errors.append("\"Appointments Over Hour\" key not found in \"Consumer Metrics\" dictionary")
                elif consumer_metrics["Appointments Over Hour"] is None:
                    post_errors.append("Value for \"Appointments Over Hour\" in \"Consumer Metrics\" dict is Null")
                else:
                    rqst_cons_apts_over_hour = int(consumer_metrics["Appointments Over Hour"])

                if "Appointments Complex Market" not in consumer_metrics:
                    post_errors.append("\"Appointments Complex Market\" key not found in \"Consumer Metrics\" dictionary")
                elif consumer_metrics["Appointments Complex Market"] is None:
                    post_errors.append("Value for \"Appointments Complex Market\" in \"Consumer Metrics\" dict is Null")
                else:
                    rqst_cons_apts_cplx_market = int(consumer_metrics["Appointments Complex Market"])

                if "Appointments Complex Medicaid" not in consumer_metrics:
                    post_errors.append("\"Appointments Complex Medicaid\" key not found in \"Consumer Metrics\" dictionary")
                elif consumer_metrics["Appointments Complex Medicaid"] is None:
                    post_errors.append("Value for \"Appointments Complex Medicaid\" in \"Consumer Metrics\" dict is Null")
                else:
                    rqst_cons_apts_cplx_maid = int(consumer_metrics["Appointments Complex Medicaid"])

                if "Appointments Post-Enrollment Assistance" not in consumer_metrics:
                    post_errors.append("\"Appointments Post-Enrollment Assistance\" key not found in \"Consumer Metrics\" dictionary")
                elif consumer_metrics["Appointments Post-Enrollment Assistance"] is None:
                    post_errors.append("Value for \"Appointments Post-Enrollment Assistance\" in \"Consumer Metrics\" dict is Null")
                else:
                    rqst_cons_apts_postenr_assis = int(consumer_metrics["Appointments Complex Medicaid"])

                if "Appointments Over 3 Hours" not in consumer_metrics:
                    post_errors.append("\"Appointments Over 3 Hours\" key not found in \"Consumer Metrics\" dictionary")
                elif consumer_metrics["Appointments Over 3 Hours"] is None:
                    post_errors.append("Value for \"Appointments Over 3 Hours\" in \"Consumer Metrics\" dict is Null")
                else:
                    rqst_cons_apts_over_3_hours = int(consumer_metrics["Appointments Over 3 Hours"])

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

        response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
        response['Access-Control-Allow-Origin'] = "*"
        return response

    elif request.method == "OPTIONS":
        response = HttpResponse("")
        response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Methods'] = "POST, OPTIONS, GET"
        response['Access-Control-Allow-Headers'] = "X-Requested-With"
        response['Access-Control-Max-Age'] = "1800"
        return response

    # if a GET request is made, add error message to response data
    else:
        response_raw_data["status"]["Error Code"] = 1
        post_errors.append("Request needs POST data")
        response_raw_data["status"]["Errors"] = post_errors
        for message in post_errors:
            print message
            sys.stdout.flush()

        response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
        response['Access-Control-Allow-Origin'] = "*"
        return response
