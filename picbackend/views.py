"""
Defines views that are mapped to url configurations
"""

from django.http import HttpResponse
from django.shortcuts import render
from django.db import models, IntegrityError
from picmodels.models import PICStaff, MetricsSubmission, PlanStat, PICConsumer
import datetime, json, sys, re, pokitdok
from django.views.decorators.csrf import csrf_exempt


# defines view for home page
def index(request):
    return render(request, "home_page.html")


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


def clean_list_input(json_dict, dict_name, dict_key, post_errors):
    if dict_key not in json_dict:
        post_errors.append("{!r} key not found in {!r} dictionary".format(dict_key, dict_name))
    elif json_dict[dict_key] is None:
        post_errors.append("Value for {!r} in {!r} dictionary is Null".format(dict_key, dict_name))
    elif not isinstance(json_dict[dict_key], list):
        post_errors.append("Value for {!r} in {!r} dictionary is not a list".format(dict_key, dict_name))
    elif json_dict[dict_key] == []:
        post_errors.append("Value for {!r} in {!r} dictionary is an empty list".format(dict_key, dict_name))
    else:
        return json_dict[dict_key]
    return None


# defines view for saving scheduled appointments to the database
@csrf_exempt
def staff_edit_handler(request):
    # initialize dictionary for response data, including parsing errors
    response_raw_data = {'status': {"Error Code": 0, "Version": 1.0}}
    post_errors = []

    if request.method == 'POST' or request.is_ajax():
        post_data = request.body.decode('utf-8')
        post_json = json.loads(post_data)

        # Code to parse POSTed json request
        rqst_action = clean_json_string_input(post_json, "root", "Database Action", post_errors)

        # if there are no parsing errors, get or create database entries for consumer, location, and point of contact
        # create and save database entry for appointment
        if len(post_errors) == 0 and rqst_action == "Staff Addition":
            rqst_usr_email = clean_json_string_input(post_json, "root", "Email", post_errors)
            rqst_usr_f_name = clean_json_string_input(post_json, "root", "First Name", post_errors)
            rqst_usr_l_name = clean_json_string_input(post_json, "root", "Last Name", post_errors)
            rqst_county = clean_json_string_input(post_json, "root", "User County", post_errors)
            rqst_usr_type = clean_json_string_input(post_json, "root", "User Type", post_errors)

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
                        print(message)
                    sys.stdout.flush()
                else:
                    response_raw_data['Data'] = {"Database ID": user_instance.id}
            else:
                response_raw_data["status"]["Error Code"] = 1
                response_raw_data["status"]["Errors"] = post_errors

                for message in post_errors:
                    print(message)
                    sys.stdout.flush()

        elif len(post_errors) == 0 and rqst_action == "Staff Modification":
            rqst_usr_id = clean_json_int_input(post_json, "root", "Database ID", post_errors)
            rqst_usr_email = clean_json_string_input(post_json, "root", "Email", post_errors)
            rqst_usr_f_name = clean_json_string_input(post_json, "root", "First Name", post_errors)
            rqst_usr_l_name = clean_json_string_input(post_json, "root", "Last Name", post_errors)
            rqst_county = clean_json_string_input(post_json, "root", "User County", post_errors)
            rqst_usr_type = clean_json_string_input(post_json, "root", "User Type", post_errors)

            if len(post_errors) == 0:
                try:
                    staff_instance = PICStaff.objects.get(id=rqst_usr_id)
                    staff_instance.first_name = rqst_usr_f_name
                    staff_instance.last_name = rqst_usr_l_name
                    staff_instance.type = rqst_usr_type
                    staff_instance.county = rqst_county
                    staff_instance.email = rqst_usr_email
                    staff_instance.save()
                    response_raw_data['Data'] = {"Database ID": staff_instance.id}
                except PICStaff.DoesNotExist:
                    post_errors.append('Staff database entry does not exist for the id: {!s}'.format(str(rqst_usr_id)))
                    response_raw_data["status"]["Error Code"] = 1
                    response_raw_data["status"]["Errors"] = post_errors

                    for message in post_errors:
                        print(message)
                    sys.stdout.flush()
                except PICStaff.MultipleObjectsReturned:
                    post_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_usr_id)))
                    response_raw_data["status"]["Error Code"] = 1
                    response_raw_data["status"]["Errors"] = post_errors

                    for message in post_errors:
                        print(message)
                    sys.stdout.flush()
                except IntegrityError:
                    post_errors.append('Database entry already exists for the email: {!s}'.format(rqst_usr_email))
                    response_raw_data["status"]["Error Code"] = 1
                    response_raw_data["status"]["Errors"] = post_errors

                    for message in post_errors:
                        print(message)
                    sys.stdout.flush()

            else:
                response_raw_data["status"]["Error Code"] = 1
                response_raw_data["status"]["Errors"] = post_errors

                for message in post_errors:
                    print(message)
                    sys.stdout.flush()

        elif len(post_errors) == 0 and rqst_action == "Staff Deletion":
            rqst_usr_id = clean_json_int_input(post_json, "root", "Database ID", post_errors)

            if len(post_errors) == 0:
                try:
                    staff_instance = PICStaff.objects.get(id=rqst_usr_id)
                    staff_instance.delete()
                    response_raw_data['Data'] = {"Database ID": "Deleted"}
                except PICStaff.DoesNotExist:
                    post_errors.append('Staff database entry does not exist for the id: {!s}'.format(str(rqst_usr_id)))
                    response_raw_data["status"]["Error Code"] = 1
                    response_raw_data["status"]["Errors"] = post_errors

                    for message in post_errors:
                        print(message)
                    sys.stdout.flush()
                except PICStaff.MultipleObjectsReturned:
                    post_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_usr_id)))
                    response_raw_data["status"]["Error Code"] = 1
                    response_raw_data["status"]["Errors"] = post_errors

                    for message in post_errors:
                        print(message)
                    sys.stdout.flush()

            else:
                response_raw_data["status"]["Error Code"] = 1
                response_raw_data["status"]["Errors"] = post_errors

                for message in post_errors:
                    print(message)
                    sys.stdout.flush()


        # add parsing errors to response dictionary
        else:
            response_raw_data["status"]["Error Code"] = 1
            response_raw_data["status"]["Errors"] = post_errors

            for message in post_errors:
                print(message)
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


@csrf_exempt
def consumer_edit_handler(request):
    # initialize dictionary for response data, including parsing errors
    response_raw_data = {'status': {"Error Code": 0, "Version": 1.0}}
    post_errors = []

    if request.method == 'POST' or request.is_ajax():
        post_data = request.body.decode('utf-8')
        post_json = json.loads(post_data)

        # Code to parse POSTed json request
        rqst_action = clean_json_string_input(post_json, "root", "Database Action", post_errors)

        # if there are no parsing errors, get or create database entries for consumer
        if len(post_errors) == 0 and rqst_action == "Consumer Addition":
            rqst_consumer_email = clean_json_string_input(post_json, "root", "Email", post_errors)
            rqst_consumer_f_name = clean_json_string_input(post_json, "root", "First Name", post_errors)
            rqst_consumer_m_name = clean_json_string_input(post_json, "root", "Middle Name", post_errors, empty_string_allowed=True)
            rqst_consumer_l_name = clean_json_string_input(post_json, "root", "Last Name", post_errors)
            rqst_consumer_zipcode = clean_json_string_input(post_json, "root", "Zipcode", post_errors)
            rqst_consumer_address = clean_json_string_input(post_json, "root", "Address", post_errors, empty_string_allowed=True)
            rqst_consumer_plan = clean_json_string_input(post_json, "root", "Plan", post_errors, empty_string_allowed=True)
            rqst_consumer_met_nav_at = clean_json_string_input(post_json, "root", "Met Navigator At", post_errors)
            rqst_consumer_household_size = clean_json_int_input(post_json, "root", "Household Size", post_errors)
            rqst_consumer_phone = clean_json_string_input(post_json, "root", "Phone Number", post_errors, empty_string_allowed=True)
            rqst_consumer_pref_lang = clean_json_string_input(post_json, "root", "Preferred Language", post_errors, empty_string_allowed=True)
            rqst_nav_id = clean_json_int_input(post_json, "root", "Navigator Database ID", post_errors)

            if len(post_errors) == 0:
                consumer_rqst_values = {"first_name": rqst_consumer_f_name,
                                        "middle_name": rqst_consumer_m_name,
                                        "last_name": rqst_consumer_l_name,
                                        "phone": rqst_consumer_phone,
                                        "zipcode": rqst_consumer_zipcode,
                                        "address": rqst_consumer_address,
                                        "plan": rqst_consumer_plan,
                                        "met_nav_at": rqst_consumer_met_nav_at,
                                        "household_size": rqst_consumer_household_size,
                                        "preferred_language": rqst_consumer_pref_lang}
                consumer_instance, consumer_instance_created = PICConsumer.objects.get_or_create(email=rqst_consumer_email,
                                                                                                 defaults=consumer_rqst_values)
                if not consumer_instance_created:
                    post_errors.append('Consumer database entry already exists for the email: {!s}'.format(rqst_consumer_email))
                    response_raw_data["status"]["Error Code"] = 1
                    response_raw_data["status"]["Errors"] = post_errors

                    for message in post_errors:
                        print(message)
                    sys.stdout.flush()
                else:
                    try:
                        nav_instance = PICStaff.objects.get(id=rqst_nav_id)
                        consumer_instance.navigator = nav_instance
                        consumer_instance.save()
                        response_raw_data['Data'] = {"Database ID": consumer_instance.id}
                    except PICStaff.DoesNotExist:
                        post_errors.append('Staff database entry does not exist for the navigator id: {!s}'.format(str(rqst_nav_id)))
                        response_raw_data["status"]["Error Code"] = 1
                        response_raw_data["status"]["Errors"] = post_errors

                        for message in post_errors:
                            print(message)
                        sys.stdout.flush()
            else:
                response_raw_data["status"]["Error Code"] = 1
                response_raw_data["status"]["Errors"] = post_errors

                for message in post_errors:
                    print(message)
                    sys.stdout.flush()

        elif len(post_errors) == 0 and rqst_action == "Consumer Modification":
            rqst_consumer_email = clean_json_string_input(post_json, "root", "Email", post_errors)
            rqst_consumer_f_name = clean_json_string_input(post_json, "root", "First Name", post_errors)
            rqst_consumer_m_name = clean_json_string_input(post_json, "root", "Middle Name", post_errors, empty_string_allowed=True)
            rqst_consumer_l_name = clean_json_string_input(post_json, "root", "Last Name", post_errors)
            rqst_consumer_zipcode = clean_json_string_input(post_json, "root", "Zipcode", post_errors)
            rqst_consumer_address = clean_json_string_input(post_json, "root", "Address", post_errors, empty_string_allowed=True)
            rqst_consumer_plan = clean_json_string_input(post_json, "root", "Plan", post_errors, empty_string_allowed=True)
            rqst_consumer_met_nav_at = clean_json_string_input(post_json, "root", "Met Navigator At", post_errors)
            rqst_consumer_household_size = clean_json_int_input(post_json, "root", "Household Size", post_errors)
            rqst_consumer_phone = clean_json_string_input(post_json, "root", "Phone Number", post_errors, empty_string_allowed=True)
            rqst_consumer_pref_lang = clean_json_string_input(post_json, "root", "Preferred Language", post_errors, empty_string_allowed=True)
            rqst_nav_id = clean_json_int_input(post_json, "root", "Navigator Database ID", post_errors)
            rqst_consumer_id = clean_json_int_input(post_json, "root", "Consumer Database ID", post_errors)

            if len(post_errors) == 0:
                try:
                    consumer_instance = PICConsumer.objects.get(id=rqst_consumer_id)
                    consumer_instance.first_name = rqst_consumer_f_name
                    consumer_instance.middle_name = rqst_consumer_m_name
                    consumer_instance.last_name = rqst_consumer_l_name
                    consumer_instance.phone = rqst_consumer_phone
                    consumer_instance.zipcode = rqst_consumer_zipcode
                    consumer_instance.address = rqst_consumer_address
                    consumer_instance.plan = rqst_consumer_plan
                    consumer_instance.met_nav_at = rqst_consumer_met_nav_at
                    consumer_instance.household_size = rqst_consumer_household_size
                    consumer_instance.preferred_language = rqst_consumer_pref_lang
                    consumer_instance.email = rqst_consumer_email

                    nav_instance = PICStaff.objects.get(id=rqst_nav_id)
                    consumer_instance.navigator = nav_instance

                    consumer_instance.save()
                    response_raw_data['Data'] = {"Database ID": consumer_instance.id}
                except PICConsumer.DoesNotExist:
                    post_errors.append('Consumer database entry does not exist for the id: {!s}'.format(str(rqst_consumer_id)))
                    response_raw_data["status"]["Error Code"] = 1
                    response_raw_data["status"]["Errors"] = post_errors

                    for message in post_errors:
                        print(message)
                    sys.stdout.flush()
                except PICConsumer.MultipleObjectsReturned:
                    post_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_consumer_id)))
                    response_raw_data["status"]["Error Code"] = 1
                    response_raw_data["status"]["Errors"] = post_errors

                    for message in post_errors:
                        print(message)
                    sys.stdout.flush()
                except IntegrityError:
                    post_errors.append('Database entry already exists for the id: {!s}'.format(str(rqst_consumer_id)))
                    response_raw_data["status"]["Error Code"] = 1
                    response_raw_data["status"]["Errors"] = post_errors

                    for message in post_errors:
                        print(message)
                    sys.stdout.flush()
                except PICStaff.DoesNotExist:
                    post_errors.append('Staff database entry does not exist for the navigator id: {!s}'.format(str(rqst_nav_id)))
                    response_raw_data["status"]["Error Code"] = 1
                    response_raw_data["status"]["Errors"] = post_errors

                    for message in post_errors:
                        print(message)
                    sys.stdout.flush()

            else:
                response_raw_data["status"]["Error Code"] = 1
                response_raw_data["status"]["Errors"] = post_errors

                for message in post_errors:
                    print(message)
                    sys.stdout.flush()

        elif len(post_errors) == 0 and rqst_action == "Consumer Deletion":
            rqst_consumer_id = clean_json_int_input(post_json, "root", "Consumer Database ID", post_errors)

            if len(post_errors) == 0:
                try:
                    consumer_instance = PICConsumer.objects.get(id=rqst_consumer_id)
                    consumer_instance.delete()
                    response_raw_data['Data'] = {"Database ID": "Deleted"}
                except PICConsumer.DoesNotExist:
                    post_errors.append('Consumer database entry does not exist for the id: {!s}'.format(str(rqst_consumer_id)))
                    response_raw_data["status"]["Error Code"] = 1
                    response_raw_data["status"]["Errors"] = post_errors

                    for message in post_errors:
                        print(message)
                    sys.stdout.flush()
                except PICConsumer.MultipleObjectsReturned:
                    post_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_consumer_id)))
                    response_raw_data["status"]["Error Code"] = 1
                    response_raw_data["status"]["Errors"] = post_errors

                    for message in post_errors:
                        print(message)
                    sys.stdout.flush()

            else:
                response_raw_data["status"]["Error Code"] = 1
                response_raw_data["status"]["Errors"] = post_errors

                for message in post_errors:
                    print(message)
                    sys.stdout.flush()


        # add parsing errors to response dictionary
        else:
            response_raw_data["status"]["Error Code"] = 1
            response_raw_data["status"]["Errors"] = post_errors

            for message in post_errors:
                print(message)
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


# defines view for saving scheduled appointments to the database
@csrf_exempt
def metrics_submission_handler(request):
    # initialize dictionary for response data, including parsing errors
    response_raw_data = {'status': {"Error Code": 0, "Version": 1.0}}
    post_errors = []

    if request.method == 'POST' or request.is_ajax():
        post_data = request.body.decode('utf-8')
        post_json = json.loads(post_data)

        # Code to parse POSTed json request
        rqst_usr_email = clean_json_string_input(post_json, "root", "Email", post_errors)

        consumer_metrics = clean_dict_input(post_json, "root", "Consumer Metrics", post_errors)
        if consumer_metrics is not None:
            consumer_metrics = post_json["Consumer Metrics"]

            rqst_cons_rec_edu = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Received Education",
                                                     post_errors)
            rqst_cons_app_maid = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Applied Medicaid",
                                                      post_errors)
            rqst_cons_sel_qhp = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Selected QHP", post_errors)
            rqst_cons_ref_maidorchip = clean_json_int_input(consumer_metrics, "Consumer Metrics",
                                                            "Referred Medicaid or CHIP", post_errors)
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
            rqst_usr_outr_act = clean_json_string_input(consumer_metrics, "Consumer Metrics",
                                                                "Outreach Activities", post_errors,
                                                                empty_string_allowed=True, none_allowed=True)
            rqst_metrics_county = clean_json_string_input(consumer_metrics, "Consumer Metrics", "County", post_errors)
            rqst_metrics_zipcode = clean_json_string_input(consumer_metrics, "Consumer Metrics", "Zipcode", post_errors)

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
                user_instance = PICStaff.objects.get(email__iexact=rqst_usr_email)

                try:
                    metrics_instance = MetricsSubmission.objects.get(staff_member=user_instance, submission_date=metrics_date)
                    response_raw_data["status"]["Message"] = ['Metrics Entry Updated']
                except models.ObjectDoesNotExist:
                    metrics_instance = MetricsSubmission(staff_member=user_instance, submission_date=metrics_date)
                    response_raw_data["status"]["Message"] = ['Metrics Entry Created']
                except MetricsSubmission.MultipleObjectsReturned:
                    response_raw_data["status"]["Error Code"] = 1
                    post_errors.append("Multiple metrics entries exist for this date")
                    response_raw_data["status"]["Errors"] = post_errors
                    for message in post_errors:
                        print(message)
                    sys.stdout.flush()
                    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
                    return response
                metrics_instance.received_education = rqst_cons_rec_edu
                metrics_instance.applied_medicaid = rqst_cons_app_maid
                metrics_instance.selected_qhp = rqst_cons_sel_qhp
                metrics_instance.ref_medicaid_or_chip = rqst_cons_ref_maidorchip
                metrics_instance.filed_exemptions = rqst_cons_filed_exemptions
                metrics_instance.rec_postenroll_support = rqst_cons_rec_postenr_support
                metrics_instance.trends = rqst_cons_trends
                metrics_instance.success_story = rqst_cons_success_story
                metrics_instance.hardship_or_difficulty = rqst_cons_hard_or_diff
                metrics_instance.outreach_activity = rqst_usr_outr_act
                metrics_instance.county = rqst_metrics_county
                metrics_instance.zipcode = rqst_metrics_zipcode

                metrics_instance.save()

                rqst_plan_stats = clean_list_input(consumer_metrics, "Consumer Metrics", "Plan Stats", post_errors)
                metrics_instance_plan_stats = metrics_instance.plan_stats.all()
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
                            planstatobject.save()
                            metrics_instance.plan_stats.add(planstatobject)
                    metrics_instance.save()
                    # for plan, enrollments in rqst_plan_stats.iteritems():
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

                    if len(post_errors) > 0:
                        response_raw_data["status"]["Error Code"] = 1
                        response_raw_data["status"]["Errors"] = post_errors

                        for message in post_errors:
                            print(message)
                            sys.stdout.flush()

            except models.ObjectDoesNotExist:
                response_raw_data["status"]["Error Code"] = 1
                post_errors.append("Staff database entry does not exist for email: {!s}".format(rqst_usr_email))
                response_raw_data["status"]["Errors"] = post_errors
                for message in post_errors:
                    print(message)
                sys.stdout.flush()

        # add parsing errors to response dictionary
        else:
            response_raw_data["status"]["Error Code"] = 1
            response_raw_data["status"]["Errors"] = post_errors

            for message in post_errors:
                print(message)
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


# defines view for returning staff data from api requests
def staff_api_handler(request):
    rqst_params = request.GET
    if 'fname' in rqst_params:
        rqst_first_name = rqst_params['fname']
        list_of_first_names = re.findall(r"[\w. '-]+", rqst_first_name)
    else:
        rqst_first_name = None
        list_of_first_names = None
    if 'lname' in rqst_params:
        rqst_last_name = rqst_params['lname']
        list_of_last_names = re.findall(r"[\w. '-]+", rqst_last_name)
    else:
        rqst_last_name = None
        list_of_last_names = None
    if 'email' in rqst_params:
        rqst_email = rqst_params['email']
        list_of_emails = re.findall(r"[@\w. '-]+", rqst_email)
    else:
        rqst_email = None
        list_of_emails = None
    if 'id' in rqst_params:
        rqst_staff_id = rqst_params['id']
        if rqst_staff_id != "all":
            list_of_ids = re.findall("\d+", rqst_staff_id)
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
        else:
            list_of_ids = None
    else:
        rqst_staff_id = None
        list_of_ids = None

    response_raw_data = {'Status': {"Error Code": 0, "Version": 1.0}}
    rqst_errors = []

    staff_members = PICStaff.objects.all()
    if rqst_first_name and rqst_last_name:
        staff_members = staff_members.filter(first_name__iexact=rqst_first_name, last_name__iexact=rqst_last_name)
        if len(staff_members) > 0:
            staff_member_dict = {}
            rqst_full_name = rqst_first_name + " " + rqst_last_name
            for staff_member in staff_members:
                if rqst_full_name not in staff_member_dict:
                    staff_member_dict[rqst_full_name] = [staff_member.return_values_dict()]
                else:
                    staff_member_dict[rqst_full_name].append(staff_member.return_values_dict())

            staff_member_list = []
            for staff_key, staff_entry in staff_member_dict.iteritems():
                staff_member_list.append(staff_entry)
            response_raw_data["Data"] = staff_member_list
        else:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('Staff Member with name: {!s} {!s} not found in database'.format(rqst_first_name,
                                                                                                rqst_last_name))
    elif list_of_emails and rqst_email:
        staff_dict = {}
        for email in list_of_emails:
            staff_members = PICStaff.objects.filter(email__iexact=email)
            for staff_member in staff_members:
                if email not in staff_dict:
                    staff_dict[email] = [staff_member.return_values_dict()]
                else:
                    staff_dict[email].append(staff_member.return_values_dict())
        if len(staff_dict) > 0:
            staff_list = []
            for staff_key, staff_entry in staff_dict.iteritems():
                staff_list.append(staff_entry)
            response_raw_data["Data"] = staff_list
            for email in list_of_emails:
                if email not in staff_dict:
                    if response_raw_data['Status']['Error Code'] != 2:
                        response_raw_data['Status']['Error Code'] = 2
                    rqst_errors.append('Staff Member with email: {!s} not found in database'.format(email))
        else:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('Staff Member with emails(s): {!s} not found in database'.format(rqst_email))

    elif rqst_first_name and list_of_first_names:
        staff_dict = {}
        for first_name in list_of_first_names:
            staff_members = PICStaff.objects.filter(first_name__iexact=first_name)
            for staff_member in staff_members:
                if first_name not in staff_dict:
                    staff_dict[first_name] = [staff_member.return_values_dict()]
                else:
                    staff_dict[first_name].append(staff_member.return_values_dict())
        if len(staff_dict) > 0:
            staff_list = []
            for staff_key, staff_entry in staff_dict.iteritems():
                staff_list.append(staff_entry)
            response_raw_data["Data"] = staff_list
            for name in list_of_first_names:
                if name not in staff_dict:
                    if response_raw_data['Status']['Error Code'] != 2:
                        response_raw_data['Status']['Error Code'] = 2
                    rqst_errors.append('Staff Member with first name: {!s} not found in database'.format(name))
        else:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('Staff Member with first name(s): {!s} not found in database'.format(rqst_first_name))

    elif rqst_last_name and list_of_last_names:
        staff_dict = {}
        for last_name in list_of_last_names:
            staff_members = PICStaff.objects.filter(last_name__iexact=last_name)
            for staff_member in staff_members:
                if last_name not in staff_dict:
                    staff_dict[last_name] = [staff_member.return_values_dict()]
                else:
                    staff_dict[last_name].append(staff_member.return_values_dict())
        if len(staff_dict) > 0:
            staff_list = []
            for staff_key, staff_entry in staff_dict.iteritems():
                staff_list.append(staff_entry)
            response_raw_data["Data"] = staff_list
            for name in list_of_last_names:
                if name not in staff_dict:
                    if response_raw_data['Status']['Error Code'] != 2:
                        response_raw_data['Status']['Error Code'] = 2
                    rqst_errors.append('Staff Member with last name: {!s} not found in database'.format(name))
        else:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('Staff Member with last name(s): {!s} not found in database'.format(rqst_last_name))

    elif rqst_staff_id:
        if rqst_staff_id == "all":
            all_staff_members = PICStaff.objects.all()
            staff_member_dict = {}
            for staff_member in all_staff_members:
                staff_member_dict[staff_member.id] = staff_member.return_values_dict()
            staff_list = []
            for staff_key, staff_entry in staff_member_dict.iteritems():
                staff_list.append(staff_entry)
            response_raw_data["Data"] = staff_list
        elif list_of_ids:
            if len(list_of_ids) > 0:
                for indx, element in enumerate(list_of_ids):
                    list_of_ids[indx] = int(element)
                staff_members = PICStaff.objects.filter(id__in=list_of_ids)
                if len(staff_members) > 0:
                    staff_dict = {}
                    for staff_member in staff_members:
                        staff_dict[staff_member.id] = staff_member.return_values_dict()
                    staff_list = []
                    for staff_key, staff_entry in staff_dict.iteritems():
                        staff_list.append(staff_entry)
                    response_raw_data["Data"] = staff_list
                    # response_raw_data["Data"] = staff_dict

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


def consumer_api_handler(request):
    rqst_params = request.GET
    if 'fname' in rqst_params:
        rqst_first_name = rqst_params['fname']
        list_of_first_names = re.findall(r"[\w. '-]+", rqst_first_name)
    else:
        rqst_first_name = None
        list_of_first_names = None
    if 'lname' in rqst_params:
        rqst_last_name = rqst_params['lname']
        list_of_last_names = re.findall(r"[\w. '-]+", rqst_last_name)
    else:
        rqst_last_name = None
        list_of_last_names = None
    if 'email' in rqst_params:
        rqst_email = rqst_params['email']
        list_of_emails = re.findall(r"[@\w. '-]+", rqst_email)
    else:
        rqst_email = None
        list_of_emails = None
    if 'id' in rqst_params:
        rqst_consumer_id = rqst_params['id']
        if rqst_consumer_id != "all":
            list_of_ids = re.findall("\d+", rqst_consumer_id)
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
        else:
            list_of_ids = None
    else:
        rqst_consumer_id = None
        list_of_ids = None
    if 'navid' in rqst_params:
        rqst_nav_id = rqst_params['navid']
        list_of_nav_ids = re.findall("\d+", rqst_nav_id)
        for indx, element in enumerate(list_of_nav_ids):
            list_of_nav_ids[indx] = int(element)
    else:
        rqst_nav_id = None
        list_of_nav_ids = None

    response_raw_data = {'Status': {"Error Code": 0, "Version": 1.0}}
    rqst_errors = []

    consumers = PICConsumer.objects.all()
    if rqst_first_name and rqst_last_name:
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
            for consumer_key, consumer_entry in consumer_dict.iteritems():
                consumer_list.append(consumer_entry)
            response_raw_data["Data"] = consumer_list
        else:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('Consumer with name: {!s} {!s} not found in database'.format(rqst_first_name,
                                                                                                rqst_last_name))
    elif list_of_emails and rqst_email:
        consumer_dict = {}
        for email in list_of_emails:
            consumers = PICConsumer.objects.filter(email__iexact=email)
            for consumer in consumers:
                if email not in consumer_dict:
                    consumer_dict[email] = [consumer.return_values_dict()]
                else:
                    consumer_dict[email].append(consumer.return_values_dict())
        if len(consumer_dict) > 0:
            consumer_list = []
            for consumer_key, consumer_entry in consumer_dict.iteritems():
                consumer_list.append(consumer_entry)
            response_raw_data["Data"] = consumer_list
            for email in list_of_emails:
                if email not in consumer_dict:
                    if response_raw_data['Status']['Error Code'] != 2:
                        response_raw_data['Status']['Error Code'] = 2
                    rqst_errors.append('Consumer with email: {!s} not found in database'.format(email))
        else:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('Consumer with emails(s): {!s} not found in database'.format(rqst_email))

    elif rqst_first_name and list_of_first_names:
        consumer_dict = {}
        for first_name in list_of_first_names:
            consumers = PICConsumer.objects.filter(first_name__iexact=first_name)
            for consumer in consumers:
                if first_name not in consumer_dict:
                    consumer_dict[first_name] = [consumer.return_values_dict()]
                else:
                    consumer_dict[first_name].append(consumer.return_values_dict())
        if len(consumer_dict) > 0:
            consumer_list = []
            for consumer_key, consumer_entry in consumer_dict.iteritems():
                consumer_list.append(consumer_entry)
            response_raw_data["Data"] = consumer_list
            for name in list_of_first_names:
                if name not in consumer_dict:
                    if response_raw_data['Status']['Error Code'] != 2:
                        response_raw_data['Status']['Error Code'] = 2
                    rqst_errors.append('Consumer with first name: {!s} not found in database'.format(name))
        else:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('Consumer with first name(s): {!s} not found in database'.format(rqst_first_name))

    elif rqst_last_name and list_of_last_names:
        consumer_dict = {}
        for last_name in list_of_last_names:
            consumers = PICConsumer.objects.filter(last_name__iexact=last_name)
            for consumer in consumers:
                if last_name not in consumer_dict:
                    consumer_dict[last_name] = [consumer.return_values_dict()]
                else:
                    consumer_dict[last_name].append(consumer.return_values_dict())
        if len(consumer_dict) > 0:
            consumer_list = []
            for consumer_key, consumer_entry in consumer_dict.iteritems():
                consumer_list.append(consumer_entry)
            response_raw_data["Data"] = consumer_list
            for name in list_of_last_names:
                if name not in consumer_dict:
                    if response_raw_data['Status']['Error Code'] != 2:
                        response_raw_data['Status']['Error Code'] = 2
                    rqst_errors.append('Staff Member with last name: {!s} not found in database'.format(name))
        else:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('Staff Member with last name(s): {!s} not found in database'.format(rqst_last_name))

    elif rqst_consumer_id:
        if rqst_consumer_id == "all":
            all_consumers = PICConsumer.objects.all()
            consumer_dict = {}
            for consumer in all_consumers:
                consumer_dict[consumer.id] = consumer.return_values_dict()
            consumer_list = []
            for consumer_key, consumer_entry in consumer_dict.iteritems():
                consumer_list.append(consumer_entry)
            response_raw_data["Data"] = consumer_list
        elif list_of_ids:
            if len(list_of_ids) > 0:
                for indx, element in enumerate(list_of_ids):
                    list_of_ids[indx] = int(element)
                consumers = PICConsumer.objects.filter(id__in=list_of_ids)
                if len(consumers) > 0:
                    consumer_dict = {}
                    for consumer in consumers:
                        consumer_dict[consumer.id] = consumer.return_values_dict()
                    consumer_list = []
                    for consumer_key, consumer_entry in consumer_dict.iteritems():
                        consumer_list.append(consumer_entry)
                    response_raw_data["Data"] = consumer_list

                    for consumer_id in list_of_ids:
                        if consumer_id not in consumer_dict:
                            if response_raw_data['Status']['Error Code'] != 2:
                                response_raw_data['Status']['Error Code'] = 2
                            rqst_errors.append('Consumer with id: {!s} not found in database'.format(str(consumer_id)))
                else:
                    response_raw_data['Status']['Error Code'] = 1
                    rqst_errors.append('No consumers found for database ID(s): ' + rqst_consumer_id)
            else:
                response_raw_data['Status']['Error Code'] = 1
                rqst_errors.append('No valid consumer IDs provided in request (must be integers)')
    elif rqst_nav_id:
        if list_of_nav_ids:
            if len(list_of_nav_ids) > 0:
                for indx, element in enumerate(list_of_nav_ids):
                    list_of_nav_ids[indx] = int(element)
                consumers = PICConsumer.objects.filter(navigator__in=list_of_nav_ids)
                if len(consumers) > 0:
                    nav_dict = {}
                    for consumer in consumers:
                        if consumer.navigator.id not in nav_dict:
                            nav_dict[consumer.navigator.id] = [consumer.return_values_dict()]
                        else:
                            nav_dict[consumer.navigator.id].append(consumer.return_values_dict())
                    nav_list = []
                    for nav_key, consumer_list in nav_dict.iteritems():
                        nav_list_entry = {"Navigator ID" : nav_key,
                                          "Consumer List": consumer_list}
                        nav_list.append(nav_list_entry)
                    response_raw_data["Data"] = nav_list

                    for nav_id in list_of_nav_ids:
                        if nav_id not in nav_dict:
                            if response_raw_data['Status']['Error Code'] != 2:
                                response_raw_data['Status']['Error Code'] = 2
                            rqst_errors.append('No consumers found for navigator with id: {!s} found in database'.format(str(nav_id)))
                else:
                    response_raw_data['Status']['Error Code'] = 1
                    rqst_errors.append('No consumers found for navigator with id(s): {!s} found in database' + rqst_nav_id)
            else:
                response_raw_data['Status']['Error Code'] = 1
                rqst_errors.append('No valid navigator IDs provided in request (must be integers)')

    else:
        response_raw_data['Status']['Error Code'] = 1
        rqst_errors.append('No Valid Parameters')

    response_raw_data["Status"]["Errors"] = rqst_errors
    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response

@csrf_exempt
def eligibility_handler(request):
    # initialize dictionary for response data, including parsing errors
    response_raw_data = {'status': {"Error Code": 0, "Version": 1.0}}
    post_errors = []

    if request.method == 'POST' or request.is_ajax():
        post_data = request.body.decode('utf-8')
        post_json = json.loads(post_data)

        rqst_consumer_f_name = clean_json_string_input(post_json, "root", "First Name", post_errors)
        rqst_consumer_l_name = clean_json_string_input(post_json, "root", "Last Name", post_errors)
        rqst_consumer_birth = clean_json_string_input(post_json, "root", "Birth Date", post_errors)

        # if no errors, make request to pokitdok
        if len(post_errors) == 0:
            pd = pokitdok.api.connect('fbSgQ0sM3xQNI5m8TyxR', 'du6JkRfNcHt8wNashtpf7Mdr96thZyn8Kilo9xoB')
            eligibility_results = pd.eligibility({
                "member": {
                    "birth_date": rqst_consumer_birth,
                    "first_name": rqst_consumer_f_name,
                    "last_name": rqst_consumer_l_name,
                },
                "trading_partner_id": "MOCKPAYER"
            })
            response_raw_data["Data"] = eligibility_results

        # add parsing errors to response dictionary
        else:
            response_raw_data["status"]["Error Code"] = 1
            response_raw_data["status"]["Errors"] = post_errors

            for message in post_errors:
                print(message)
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

    elif grouping_parameter == "Zipcode":
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
    response_raw_data = {'Status': {"Error Code": 0, "Version": 1.0}}
    rqst_errors = []

    if "id" in rqst_params:
        rqst_staff_id = rqst_params["id"]
        list_of_ids = re.findall("\d+", rqst_staff_id)
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
    else:
        rqst_staff_id = None
        list_of_ids = None

    if "fname" in rqst_params:
        rqst_fname = rqst_params["fname"]
        list_of_first_names = re.findall("[\w. '-]+", rqst_params['fname'])
    else:
        rqst_fname = None
        list_of_first_names = None

    if "lname" in rqst_params:
        rqst_lname = rqst_params["lname"]
        list_of_last_names = re.findall("[\w. '-]+", rqst_params['lname'])
    else:
        rqst_lname = None
        list_of_last_names = None

    if "email" in rqst_params:
        rqst_staff_email = rqst_params["email"]
        list_of_emails = re.findall(r"[@\w. '-]+", rqst_params['email'])
    else:
        rqst_staff_email = None
        list_of_emails = None

    if "county" in rqst_params:
        rqst_counties = rqst_params["county"]
        list_of_counties = re.findall("[\w. '-]+", rqst_counties)
    else:
        list_of_counties = None

    if "zipcode" in rqst_params:
        rqst_zipcodes = rqst_params["zipcode"]
        list_of_zipcodes = re.findall("\d+", rqst_zipcodes)
    else:
        list_of_zipcodes= None

    if "time" in rqst_params:
        try:
            rqst_time = int(rqst_params["time"])
            look_up_date = datetime.date.today() - datetime.timedelta(days=rqst_time)
        except ValueError:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('time parameter must be a valid integer. Metrics returned without time parameter.')
            look_up_date = None
    else:
        look_up_date = None

    if "startdate" in rqst_params:
        try:
            rqst_start_date = rqst_params["startdate"]
            # look_up_date = datetime.date.today() - datetime.timedelta(days=rqst_time)
        except ValueError:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('time parameter must be a valid integer. Metrics returned without time parameter.')
            # look_up_date = None
    else:
        rqst_start_date = None

    if "enddate" in rqst_params:
        try:
            rqst_end_date = rqst_params["enddate"]
            # look_up_date = datetime.date.today() - datetime.timedelta(days=rqst_time)
        except ValueError:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('time parameter must be a valid integer. Metrics returned without time parameter.')
            # look_up_date = None
    else:
        rqst_end_date = None

    # Start with this query for all and then evaluate down from request params
    # Queries arent evaluated until you read the data
    metrics_submissions = MetricsSubmission.objects.all()
    if list_of_zipcodes is not None:
        metrics_submissions = metrics_submissions.filter(zipcode__in=list_of_zipcodes)
    if look_up_date:
        metrics_submissions = metrics_submissions.filter(submission_date__gte=look_up_date)
    if rqst_start_date:
        metrics_submissions = metrics_submissions.filter(submission_date__gte=rqst_start_date)
    if rqst_end_date:
        metrics_submissions = metrics_submissions.filter(submission_date__lte=rqst_end_date)

    if rqst_staff_id:
        if rqst_staff_id.lower() != "all":
            metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)

        metrics_dict = {}
        if len(metrics_submissions) > 0:
            for metrics_submission in metrics_submissions:
                if metrics_submission.staff_member_id not in metrics_dict:
                    metrics_dict[metrics_submission.staff_member_id] = {"Metrics Data": [metrics_submission.return_values_dict()]}
                    metrics_dict[metrics_submission.staff_member_id]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                else:
                    metrics_dict[metrics_submission.staff_member_id]["Metrics Data"].append(metrics_submission.return_values_dict())

            if rqst_staff_id.lower() != "all":
                for staff_id in list_of_ids:
                    if staff_id not in metrics_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Metrics for staff Member with id: {!s} not found in database'.format(str(staff_id)))
        else:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('No metrics entries for staff ID(s): {!s} not found in database'.format(rqst_staff_id))
    elif rqst_fname and rqst_lname:
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
                metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)
            else:
                if response_raw_data['Status']['Error Code'] != 2:
                    rqst_errors.append('No metrics entries for first names(s): {!s}; and last names(s): {!s} not found in database'.format(rqst_fname, rqst_lname))
                response_raw_data['Status']['Error Code'] = 1

            metrics_dict = {}
            if len(metrics_submissions) > 0:
                for metrics_submission in metrics_submissions:
                    name = '{!s} {!s}'.format(metrics_submission.staff_member.first_name, metrics_submission.staff_member.last_name)
                    if name not in metrics_dict:
                        metrics_dict[name] = {"Metrics Data": [metrics_submission.return_values_dict()]}
                        metrics_dict[name]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                    else:
                        metrics_dict[name]["Metrics Data"].append(metrics_submission.return_values_dict())
            else:
                if response_raw_data['Status']['Error Code'] != 2:
                    rqst_errors.append('No metrics entries for first names(s): {!s}; and last names(s): {!s} not found in database'.format(rqst_fname, rqst_lname))
        else:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('Length of first name list must be equal to length of last name list')
    elif rqst_fname:
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
            metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)

            metrics_dict = {}
            if len(metrics_submissions) > 0:
                for metrics_submission in metrics_submissions:
                    if metrics_submission.staff_member.first_name not in metrics_dict:
                        metrics_dict[metrics_submission.staff_member.first_name] = {"Metrics Data": [metrics_submission.return_values_dict()]}
                        metrics_dict[metrics_submission.staff_member.first_name]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                    else:
                        metrics_dict[metrics_submission.staff_member.first_name]["Metrics Data"].append(metrics_submission.return_values_dict())
            else:
                if response_raw_data['Status']['Error Code'] != 2:
                    rqst_errors.append('No metrics entries for first name(s): {!s} not found in database'.format(rqst_fname))
                response_raw_data['Status']['Error Code'] = 1
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for first name(s): {!s} not found in database'.format(rqst_fname))
            response_raw_data['Status']['Error Code'] = 1
    elif rqst_lname:
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
            metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)

            metrics_dict = {}
            if len(metrics_submissions) > 0:
                for metrics_submission in metrics_submissions:
                    if metrics_submission.staff_member.last_name not in metrics_dict:
                        metrics_dict[metrics_submission.staff_member.last_name] = {"Metrics Data": [metrics_submission.return_values_dict()]}
                        metrics_dict[metrics_submission.staff_member.last_name]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                    else:
                        metrics_dict[metrics_submission.staff_member.last_name]["Metrics Data"].append(metrics_submission.return_values_dict())
            else:
                if response_raw_data['Status']['Error Code'] != 2:
                    rqst_errors.append('No metrics entries for last name(s): {!s} not found in database'.format(rqst_lname))
                response_raw_data['Status']['Error Code'] = 1
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for last name(s): {!s} not found in database'.format(rqst_lname))
            response_raw_data['Status']['Error Code'] = 1
    elif rqst_staff_email:
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
            metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)

            metrics_dict = {}
            if len(metrics_submissions) > 0:
                for metrics_submission in metrics_submissions:
                    if metrics_submission.staff_member.email not in metrics_dict:
                        metrics_dict[metrics_submission.staff_member.email] = {"Metrics Data": [metrics_submission.return_values_dict()]}
                        metrics_dict[metrics_submission.staff_member.email]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                    else:
                        metrics_dict[metrics_submission.staff_member.email]["Metrics Data"].append(metrics_submission.return_values_dict())
            else:
                if response_raw_data['Status']['Error Code'] != 2:
                    rqst_errors.append('No metrics entries for email(s): {!s} not found in database'.format(rqst_staff_email))
                response_raw_data['Status']['Error Code'] = 1
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for email(s): {!s} not found in database'.format(rqst_staff_email))
            response_raw_data['Status']['Error Code'] = 1

    if "groupby" in rqst_params:
        if rqst_params["groupby"] == "zipcode" or rqst_params["groupby"] == "Zipcode":
            metrics_dict = group_metrics(metrics_dict, "Zipcode")
            metrics_list = []
            for metrics_key, metrics_entry in metrics_dict.iteritems():
                metrics_list.append(metrics_entry)
            response_raw_data["Data"] = metrics_list
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

    response_raw_data["Status"]["Errors"] = rqst_errors
    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response
