"""
Defines views that are mapped to url configurations
"""

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from picmodels.models import PICStaff, MetricsSubmission, PICConsumer, PlanStat, NavMetricsLocation, CredentialsModel
import json, sys, pokitdok, base64, datetime
from picbackend.forms import NavMetricsLocationForm
from django.contrib import messages
from django.forms import modelformset_factory
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from picbackend.utils.base import clean_json_string_input, init_response_data, parse_and_log_errors,\
    fetch_and_parse_pokit_elig_data, clean_list_input
from picbackend.utils.db_updates import add_staff, modify_staff, delete_staff, add_consumer, modify_consumer, delete_consumer,\
    add_or_update_metrics_entity, add_nav_hub_location, modify_nav_hub_location, delete_nav_hub_location
from picbackend.utils.db_queries import retrieve_f_l_name_staff, retrieve_email_staff, retrieve_first_name_staff,\
    retrieve_last_name_staff, retrieve_id_staff, build_search_params, retrieve_f_l_name_consumers,\
    retrieve_email_consumers, retrieve_first_name_consumers, retrieve_last_name_consumers, retrieve_id_consumers,\
    break_results_into_pages, group_metrics, retrieve_id_metrics, retrieve_f_l_name_metrics,\
    retrieve_first_name_metrics, retrieve_last_name_metrics, retrieve_email_metrics, retrieve_county_staff,\
    retrieve_region_staff, retrieve_location_metrics, retrieve_mpn_metrics, retrieve_mpn_staff

from oauth2client.client import flow_from_clientsecrets
from django.conf import settings
# from picbackend.settings import GOOGLE_OAUTH2_CLIENT_SECRETS_JSON, SECRET_KEY, HOSTURL
from oauth2client.contrib.django_util.storage import DjangoORMStorage
# from oauth2client.contrib.django_orm import Storage
from django.contrib.auth.decorators import login_required
from oauth2client.contrib import xsrfutil
import logging
import httplib2
from googleapiclient.discovery import build
from django.http import HttpResponseBadRequest
from random import shuffle
from pandas.tseries.offsets import BDay
from pandas import bdate_range
from bdateutil import isbday
import dateutil.parser
from dateutil.tz import tzutc
import pytz


FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri=(settings.HOSTURL + '/oauth2callback'))
FLOW.params['access_type'] = 'offline'
FLOW.params["prompt"] = "consent"


# @login_required
# def index(request):
#     storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
#     credential = storage.get()
#     if credential is None or credential.invalid == True:
#         FLOW.params['state'] = xsrfutil.generate_token(SECRET_KEY,
#                                                        request.user)
#         authorize_url = FLOW.step1_get_authorize_url()
#         return HttpResponseRedirect(authorize_url)
#
#     else:
#         http = httplib2.Http()
#         http = credential.authorize(http)
#         service = build("plus", "v1", http=http)
#         activities = service.activities()
#         activitylist = activities.list(collection='public',
#                                        userId='me').execute()
#         logging.info(activitylist)
#
#         return render(request, 'welcome.html', {'activitylist': activitylist,})
def index(request):
    return HttpResponse("PIC Backend Home")


def auth_return(request):
    response_raw_data, rqst_errors = init_response_data()
    search_params = build_search_params(request.GET, response_raw_data, rqst_errors)

    state_string = request.GET['state']
    state_dict = json.loads(base64.urlsafe_b64decode(state_string).decode('ascii'))
    if not xsrfutil.validate_token(settings.SECRET_KEY, bytes(state_dict['token'], 'utf-8'), state_dict["navid"]):
        return HttpResponseBadRequest()
    # if not xsrfutil.validate_token(SECRET_KEY, bytes(request.GET['state'], 'utf-8'), search_params["navigator id"]):
    #     return HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.REQUEST)
    storage = DjangoORMStorage(CredentialsModel, 'id', PICStaff.objects.get(id=state_dict["navid"]), 'credential')
    storage.put(credential)
    return HttpResponseRedirect("/v1/calendar_auth/?navid={!s}".format(state_dict["navid"]))

# # defines view for home page
# def index(request):
#     return render(request, "home_page.html")


def handle_calendar_auth_request(request):
    response_raw_data, rqst_errors = init_response_data()
    search_params = build_search_params(request.GET, response_raw_data, rqst_errors)
    if 'navigator id' in search_params:
        nav_id = search_params["navigator id"]
        try:
            picstaff_object = PICStaff.objects.get(id=nav_id)
            storage = DjangoORMStorage(CredentialsModel, 'id', nav_id, 'credential')
            credential = storage.get()
            if credential is None or credential.invalid == True:
                google_token = xsrfutil.generate_token(settings.SECRET_KEY, picstaff_object.id)
                params_dict = {"navid": nav_id,
                               "token": google_token.decode('ascii')}
                params_json = json.dumps(params_dict).encode('ascii')
                params_base64_encoded = base64.urlsafe_b64encode(params_json)
                authorize_url = FLOW.step1_get_authorize_url(state=params_base64_encoded)
                return HttpResponseRedirect(authorize_url)

            else:
                response_raw_data["Data"] = "Authorized!"
                # http = httplib2.Http()
                # http = credential.authorize(http)
                # service = build("calendar", "v3", http=http)
                # events_result = service.events().list(calendarId='primary', maxResults=10, singleEvents=True,
                #                                       orderBy='startTime').execute()
                # logging.info(events_result)
                # response_raw_data["Data"] = events_result

        except PICStaff.DoesNotExist:
            rqst_errors.append('Navigator database entry does not exist for the id: {!s}'.format(str(nav_id)))

    else:
        rqst_errors.append("No valid parameters")

    response_raw_data["Host"] = settings.HOSTURL
    response_raw_data = parse_and_log_errors(response_raw_data, rqst_errors)
    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response


def handle_location_add_request(request):
    form = NavMetricsLocationForm(request.POST or None, request.FILES or None)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        # check whether it's valid:
        if form.is_valid():
            form.save()
            form = NavMetricsLocationForm()
            messages.success(request, 'Success!')
        else:
            messages.error(request, "You done fucked up!")

    return render(request, 'nav_location_add_form.html', {'form': form})


def handle_manage_locations_request(request):
    location_form_set = modelformset_factory(NavMetricsLocation, exclude=('country', ), extra=0)
    if request.method == 'POST':
        formset = location_form_set(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Success!')
        else:
            messages.error(request, "You done fucked up!")
    else:
        formset = location_form_set()
    return render(request, 'manage_nav_locations.html', {'formset': formset})


@csrf_exempt
def handle_hub_location_edit_api_request(request):
    # initialize dictionary for response data, including parsing errors
    response_raw_data, post_errors = init_response_data()

    if request.method == 'POST' or request.is_ajax():
        post_data = request.body.decode('utf-8')
        post_json = json.loads(post_data)

        # Code to parse POSTed json request
        rqst_action = clean_json_string_input(post_json, "root", "Database Action", post_errors)

        # if there are no parsing errors, get or create database entries for consumer, location, and point of contact
        # create and save database entry for appointment
        if len(post_errors) == 0 and rqst_action == "Location Addition":
            response_raw_data = add_nav_hub_location(response_raw_data, post_json, post_errors)

        elif len(post_errors) == 0 and rqst_action == "Location Modification":
            response_raw_data = modify_nav_hub_location(response_raw_data, post_json, post_errors)

        elif len(post_errors) == 0 and rqst_action == "Location Deletion":
            response_raw_data = delete_nav_hub_location(response_raw_data, post_json, post_errors)

    # if a GET request is made, add error message to response data
    else:
        post_errors.append("Request needs POST data")

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response


@csrf_exempt
def handle_staff_edit_request(request):
    # initialize dictionary for response data, including parsing errors
    response_raw_data, post_errors = init_response_data()

    if request.method == 'POST' or request.is_ajax():
        post_data = request.body.decode('utf-8')
        post_json = json.loads(post_data)

        # Code to parse POSTed json request
        rqst_action = clean_json_string_input(post_json, "root", "Database Action", post_errors)

        # if there are no parsing errors, get or create database entries for consumer, location, and point of contact
        # create and save database entry for appointment
        if len(post_errors) == 0 and rqst_action == "Staff Addition":
            response_raw_data = add_staff(response_raw_data, post_json, post_errors)

        elif len(post_errors) == 0 and rqst_action == "Staff Modification":
            response_raw_data = modify_staff(response_raw_data, post_json, post_errors)

        elif len(post_errors) == 0 and rqst_action == "Staff Deletion":
            response_raw_data = delete_staff(response_raw_data, post_json, post_errors)

    # if a GET request is made, add error message to response data
    else:
        post_errors.append("Request needs POST data")

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response


@csrf_exempt
def handle_consumer_edit_request(request):
    # initialize dictionary for response data, including parsing errors
    response_raw_data, post_errors = init_response_data()

    if request.method == 'POST' or request.is_ajax():
        post_data = request.body.decode('utf-8')
        post_json = json.loads(post_data)

        # Code to parse POSTed json request
        rqst_action = clean_json_string_input(post_json, "root", "Database Action", post_errors)

        # if there are no parsing errors, get or create database entries for consumer
        if len(post_errors) == 0 and rqst_action == "Consumer Addition":
            response_raw_data = add_consumer(response_raw_data, post_json, post_errors)

        elif len(post_errors) == 0 and rqst_action == "Consumer Modification":
            response_raw_data = modify_consumer(response_raw_data, post_json, post_errors)

        elif len(post_errors) == 0 and rqst_action == "Consumer Deletion":
            response_raw_data = delete_consumer(response_raw_data, post_json, post_errors)

    # if a GET request is made, add error message to response data
    else:
        post_errors.append("Request needs POST data")

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response


@csrf_exempt
def handle_metrics_submission_request(request):
    # initialize dictionary for response data, including parsing errors
    response_raw_data, post_errors = init_response_data()

    if request.method == 'POST' or request.is_ajax():
        post_data = request.body.decode('utf-8')
        post_json = json.loads(post_data)

        # Code to parse POSTed json request
        response_raw_data = add_or_update_metrics_entity(response_raw_data, post_json, post_errors)

    # if a GET request is made, add error message to response data
    else:
        post_errors.append("Request needs POST data")

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response


# defines view for returning staff data from api requests
def handle_staff_api_request(request):
    response_raw_data, rqst_errors = init_response_data()
    search_params = build_search_params(request.GET, response_raw_data, rqst_errors)
    staff_members = PICStaff.objects.all()

    if 'first name' in search_params and 'last name' in search_params:
        rqst_first_name = search_params['first name']
        rqst_last_name = search_params['last name']
        response_raw_data, rqst_errors = retrieve_f_l_name_staff(response_raw_data, rqst_errors, staff_members,
                                                                 rqst_first_name, rqst_last_name)
    elif 'email' in search_params:
        rqst_email = search_params['email']
        list_of_emails = search_params['email list']
        response_raw_data, rqst_errors = retrieve_email_staff(response_raw_data, rqst_errors, rqst_email,
                                                              list_of_emails)
    elif 'mpn' in search_params:
        rqst_mpn = search_params['mpn']
        list_of_mpns = search_params['mpn list']
        response_raw_data, rqst_errors = retrieve_mpn_staff(response_raw_data, rqst_errors, rqst_mpn,
                                                              list_of_mpns)
    elif 'first name' in search_params:
        rqst_first_name = search_params['first name']
        list_of_first_names = search_params['first name list']
        response_raw_data, rqst_errors = retrieve_first_name_staff(response_raw_data, rqst_errors, rqst_first_name,
                                                                   list_of_first_names)
    elif 'last name' in search_params:
        rqst_last_name = search_params['last name']
        list_of_last_names = search_params['last name list']
        response_raw_data, rqst_errors = retrieve_last_name_staff(response_raw_data, rqst_errors, rqst_last_name,
                                                                  list_of_last_names)
    elif 'county' in search_params:
        rqst_county = search_params['county']
        list_of_counties = search_params['county list']
        response_raw_data, rqst_errors = retrieve_county_staff(response_raw_data, rqst_errors, rqst_county,
                                                               list_of_counties)
    elif 'region' in search_params:
        rqst_region = search_params['region']
        list_of_regions = search_params['region list']
        response_raw_data, rqst_errors = retrieve_region_staff(response_raw_data, rqst_errors, rqst_region,
                                                               list_of_regions)
    elif 'id' in search_params:
        rqst_staff_id = search_params['id']
        if rqst_staff_id != 'all':
            list_of_ids = search_params['id list']
        else:
            list_of_ids = None
        response_raw_data, rqst_errors = retrieve_id_staff(response_raw_data, rqst_errors, rqst_staff_id, list_of_ids)
    else:
        rqst_errors.append('No Valid Parameters')

    response_raw_data = parse_and_log_errors(response_raw_data, rqst_errors)
    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response


def handle_consumer_api_request(request):
    response_raw_data, rqst_errors = init_response_data()
    search_params = build_search_params(request.GET, response_raw_data, rqst_errors)
    CONSUMERS_PER_PAGE = 20
    consumers = PICConsumer.objects.all()

    if 'navigator id list' in search_params:
        list_of_nav_ids = search_params['navigator id list']
        consumers = consumers.filter(navigator__in=list_of_nav_ids)
    if 'first name' in search_params and 'last name' in search_params:
        rqst_first_name = search_params['first name']
        rqst_last_name = search_params['last name']
        response_raw_data, rqst_errors = retrieve_f_l_name_consumers(response_raw_data, rqst_errors, consumers,
                                                                     rqst_first_name, rqst_last_name)
    elif 'email' in search_params:
        rqst_email = search_params['email']
        list_of_emails = search_params['email list']
        response_raw_data, rqst_errors = retrieve_email_consumers(response_raw_data, rqst_errors, consumers, rqst_email,
                                                                  list_of_emails)
    elif 'first name' in search_params:
        rqst_first_name = search_params['first name']
        list_of_first_names = search_params['first name list']
        response_raw_data, rqst_errors = retrieve_first_name_consumers(response_raw_data, rqst_errors, consumers,
                                                                       rqst_first_name, list_of_first_names)
    elif 'last name' in search_params:
        rqst_last_name = search_params['last name']
        list_of_last_names = search_params['last name list']
        response_raw_data, rqst_errors = retrieve_last_name_consumers(response_raw_data, rqst_errors, consumers,
                                                                      rqst_last_name, list_of_last_names)
    elif 'id' in search_params:
        rqst_consumer_id = search_params['id']
        if rqst_consumer_id != 'all':
            list_of_ids = search_params['id list']
        else:
            list_of_ids = None
        response_raw_data, rqst_errors = retrieve_id_consumers(response_raw_data, rqst_errors, consumers,
                                                               rqst_consumer_id, list_of_ids)
    else:
        rqst_errors.append('No Valid Parameters')

    if "Data" in response_raw_data:
        rqst_page_no = search_params['page number'] if 'page number' in search_params else None
        response_raw_data = break_results_into_pages(request, response_raw_data, CONSUMERS_PER_PAGE, rqst_page_no)

    response_raw_data = parse_and_log_errors(response_raw_data, rqst_errors)
    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response


@csrf_exempt
def handle_eligibility_request(request):
    # initialize dictionary for response data, including parsing errors
    response_raw_data, post_errors = init_response_data()

    if request.method == 'POST' or request.is_ajax():
        post_data = request.body.decode('utf-8')
        post_json = json.loads(post_data)

        response_raw_data = fetch_and_parse_pokit_elig_data(post_json, response_raw_data, post_errors)

    # if a GET request is made, add error message to response data
    else:
        post_errors.append("Request needs POST data")

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response


@csrf_exempt
def handle_trading_partner_request(request):
    # initialize dictionary for response data, including parsing errors
    response_raw_data, rqst_errors = init_response_data()
    search_params = build_search_params(request.GET, response_raw_data, rqst_errors)
    pd = pokitdok.api.connect('fbSgQ0sM3xQNI5m8TyxR', 'du6JkRfNcHt8wNashtpf7Mdr96thZyn8Kilo9xoB')

    # make request to pokitdok
    if "partnerid" in search_params:
        trading_partners = pd.trading_partners(search_params["partnerid"])
    else:
        trading_partners = pd.trading_partners()

    response_raw_data["Data"] = trading_partners["data"]

    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response


# defines view for returning metrics data from api requests
def handle_metrics_api_request(request):
    response_raw_data, rqst_errors = init_response_data()
    search_params = build_search_params(request.GET, response_raw_data, rqst_errors)
    metrics_dict = {}

    metrics_fields = ["Metrics Date",
                      "County",
                      "Location",
                      "no_general_assis",
                      "no_plan_usage_assis",
                      "no_locating_provider_assis",
                      "no_billing_assis",
                      "no_enroll_apps_started",
                      "no_enroll_qhp",
                      "no_enroll_abe_chip",
                      "no_enroll_shop",
                      "no_referrals_agents_brokers",
                      "no_referrals_ship_medicare",
                      "no_referrals_other_assis_programs",
                      "no_referrals_issuers",
                      "no_referrals_doi",
                      "no_mplace_tax_form_assis",
                      "no_mplace_exempt_assis",
                      "no_qhp_abe_appeals",
                      "no_data_matching_mplace_issues",
                      "no_sep_eligible",
                      "no_employ_spons_cov_issues",
                      "no_aptc_csr_assis",
                      "cmplx_cases_mplace_issues",
                      "Plan Stats"]
    validated_fields = []
    if 'fields list' in search_params:
        list_of_rqst_fields = search_params['fields list']
        while list_of_rqst_fields:
            rqst_field = list_of_rqst_fields.pop()
            if rqst_field in metrics_fields:
                validated_fields.append(rqst_field)
            else:
                rqst_errors.append("{!s} is not a valid metrics field".format(rqst_field))
        if not validated_fields:
            rqst_errors.append("No valid field parameters in request, returning all metrics fields.")

    # Start with this query for all and then evaluate down from request params
    # Queries arent evaluated until you read the data
    metrics_submissions = MetricsSubmission.objects.all()
    if 'zipcode list' in search_params:
        list_of_zipcodes = search_params['zipcode list']
        metrics_submissions = metrics_submissions.filter(location__address__zipcode__in=list_of_zipcodes)
    if 'look up date' in search_params:
        look_up_date = search_params['look up date']
        metrics_submissions = metrics_submissions.filter(submission_date__gte=look_up_date)
    if 'start date' in search_params:
        rqst_start_date = search_params['start date']
        metrics_submissions = metrics_submissions.filter(submission_date__gte=rqst_start_date)
    if 'end date' in search_params:
        rqst_end_date = search_params['end date']
        metrics_submissions = metrics_submissions.filter(submission_date__lte=rqst_end_date)
    if 'location' in search_params:
        rqst_location = search_params['location']
        metrics_submissions = metrics_submissions.filter(location__name__iexact=rqst_location)

    if 'id' in search_params:
        rqst_staff_id = search_params['id']
        if rqst_staff_id != 'all':
            list_of_ids = search_params['id list']
        else:
            list_of_ids = None
        metrics_dict = retrieve_id_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_staff_id,
                                           list_of_ids, fields=validated_fields)
    elif 'first name' in search_params and 'last name' in search_params:
        rqst_fname = search_params['first name']
        rqst_lname = search_params['last name']
        list_of_first_names = search_params['first name list']
        list_of_last_names = search_params['last name list']
        metrics_dict = retrieve_f_l_name_metrics(response_raw_data, rqst_errors, metrics_submissions,
                                                 list_of_first_names, list_of_last_names, rqst_fname, rqst_lname,
                                                 fields=validated_fields)
    elif 'first name' in search_params:
        rqst_fname = search_params['first name']
        list_of_first_names = search_params['first name list']
        metrics_dict = retrieve_first_name_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_fname,
                                                   list_of_first_names, fields=validated_fields)
    elif 'last name' in search_params:
        rqst_lname = search_params['last name']
        list_of_last_names = search_params['last name list']
        metrics_dict = retrieve_last_name_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_lname,
                                                  list_of_last_names, fields=validated_fields)
    elif 'email' in search_params:
        rqst_staff_email = search_params['email']
        list_of_emails = search_params['email list']
        metrics_dict = retrieve_email_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_staff_email,
                                              list_of_emails, fields=validated_fields)
    elif 'mpn' in search_params:
        rqst_staff_mpn = search_params['mpn']
        list_of_mpns = search_params['mpn list']
        metrics_dict = retrieve_mpn_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_staff_mpn,
                                              list_of_mpns, fields=validated_fields)
    # elif 'location' in search_params:
    #     rqst_location = search_params['location']
    #     metrics_dict = retrieve_location_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_location,
    #                                              fields=validated_fields)

    if "group by" in search_params:
        if search_params["group by"] == "zipcode" or search_params["group by"] == "Zipcode":
            metrics_dict = group_metrics(metrics_dict, "Zipcode")
            metrics_list = []
            for metrics_key, metrics_entry in metrics_dict.items():
                metrics_list.append(metrics_entry)
            response_raw_data["Data"] = metrics_list
        else:
            metrics_list = []
            for metrics_key, metrics_entry in metrics_dict.items():
                metrics_list.append(metrics_entry)
            response_raw_data["Data"] = metrics_list
            # response_raw_data["Data"] = metrics_dict
    else:
        metrics_list = []
        for metrics_key, metrics_entry in metrics_dict.items():
            metrics_list.append(metrics_entry)
        response_raw_data["Data"] = metrics_list
        # response_raw_data["Data"] = metrics_dict

    response_raw_data = parse_and_log_errors(response_raw_data, rqst_errors)
    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response


# defines view for returning navigator location data from api requests
def handle_nav_location_api_request(request):
    response_raw_data, rqst_errors = init_response_data()
    # search_params = build_search_params(request.GET, response_raw_data, rqst_errors)
    nav_location_list = []

    nav_location_entries = NavMetricsLocation.objects.all()
    for nav_location_entry in nav_location_entries:
        nav_location_list.append(nav_location_entry.return_values_dict())

    if nav_location_list:
        response_raw_data["Data"] = nav_location_list
    else:
        rqst_errors.append("No location entries found in database.")

    response_raw_data = parse_and_log_errors(response_raw_data, rqst_errors)
    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response


@csrf_exempt
def handle_nav_appointments_api_request(request):
    START_OF_BUSINESS_TIMESTAMP = datetime.time(hour=15, minute=0, second=0, microsecond=0)
    END_OF_BUSINESS_TIMESTAMP = datetime.time(hour=23, minute=0, second=0, microsecond=0)

    # initialize dictionary for response data, including parsing errors
    response_raw_data, post_errors = init_response_data()

    if request.method == 'POST' or request.is_ajax():
        post_data = request.body.decode('utf-8')
        post_json = json.loads(post_data)

        response_raw_data["Data"] = {}
        response_raw_data["Data"]["Next Available Appointments"] = []
        response_raw_data["Data"]["Preferred Appointments"] = []
        response_raw_data["Appointment Times"] = []

        rqst_preferred_times = clean_list_input(post_json, "root", "Preferred Times", post_errors, empty_list_allowed=True)

        valid_rqst_preferred_times_timestamps = []
        for preferred_time_iso_string in rqst_preferred_times:
            if isinstance(preferred_time_iso_string, str):
                try:
                    valid_rqst_preferred_times_timestamps.append(dateutil.parser.parse(preferred_time_iso_string))
                except ValueError:
                    pass

        if valid_rqst_preferred_times_timestamps:
            oldest_preferred_time_timestamp = min(valid_rqst_preferred_times_timestamps)
            max_preferred_time_timestamp = max(valid_rqst_preferred_times_timestamps) + datetime.timedelta(hours=1)

            credentials_objects = list(CredentialsModel.objects.all())
            nav_free_busy_list = []
            while credentials_objects:
                credentials_object = credentials_objects.pop()
                nav_object = credentials_object.id

                if credentials_object.credential.invalid:
                    credentials_object.delete()
                else:
                    #Obtain valid credential and use it to build authorized service object for given navigator
                    credential = credentials_object.credential
                    http = httplib2.Http()
                    http = credential.authorize(http)
                    service = build("calendar", "v3", http=http)

                    free_busy_args = {"timeMin": oldest_preferred_time_timestamp.isoformat() + 'Z', # 'Z' indicates UTC time
                                      "timeMax": max_preferred_time_timestamp.isoformat() + 'Z',
                                      "items": [{"id": "primary"}
                                                ]}
                    free_busy_result = service.freebusy().query(body=free_busy_args).execute()

                    free_busy_entry = [nav_object.return_values_dict(), free_busy_result["calendars"]["primary"]["busy"]]
                    nav_free_busy_list.append(free_busy_entry)

            for preferred_time_iso_string in rqst_preferred_times:
                shuffle(nav_free_busy_list)
                preferred_appointments_list = []

                if not isinstance(preferred_time_iso_string, str):
                    post_errors.append("{!s} is not a string, Preferred Times must be a string iso formatted date and time".format(str(preferred_time_iso_string)))
                else:
                    try:
                        preferred_time_timestamp = dateutil.parser.parse(preferred_time_iso_string).replace(tzinfo=pytz.UTC)

                        preferred_apt_entry = {"Navigator Name": None,
                                                "Navigator Database ID": None,
                                                "Appointment Date and Time": None,
                                                "Schedule Appointment Link": None,
                                                }

                        for nav_free_busy_entry in nav_free_busy_list:
                            nav_info = nav_free_busy_entry[0]
                            nav_busy_list = nav_free_busy_entry[1]
                            if not nav_busy_list:
                                preferred_apt_entry["Navigator Name"] = "{!s} {!s}".format(nav_info["First Name"],nav_info["Last Name"])
                                preferred_apt_entry["Navigator Database ID"] = nav_info["Database ID"]
                                preferred_apt_entry["Appointment Date and Time"] = preferred_time_timestamp.isoformat()[:-6]
                                preferred_apt_entry["Schedule Appointment Link"] = "http://picbackend.herokuapp.com/v1/scheduleappointment/?navid={!s}".format(str(nav_info["Database ID"]))
                                preferred_appointments_list.append(preferred_apt_entry)
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
                                    preferred_apt_entry["Navigator Name"] = "{!s} {!s}".format(nav_info["First Name"],nav_info["Last Name"])
                                    preferred_apt_entry["Navigator Database ID"] = nav_info["Database ID"]
                                    preferred_apt_entry["Appointment Date and Time"] = preferred_time_timestamp.isoformat()[:-6]
                                    preferred_apt_entry["Schedule Appointment Link"] = "http://picbackend.herokuapp.com/v1/scheduleappointment/?navid={!s}".format(str(nav_info["Database ID"]))
                                    preferred_appointments_list.append(preferred_apt_entry)
                                    break

                    except ValueError:
                        post_errors.append("{!s} is not a properly iso formatted date and time, Preferred Times must be a string iso formatted date and time".format(preferred_time_iso_string))

                response_raw_data["Data"]["Preferred Appointments"].append(preferred_appointments_list)
        else:
            now_date_time = datetime.datetime.utcnow()
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

            end_of_next_b_day_date_time = earliest_available_date_time + BDay(1)
            end_of_next_b_day_date_time = end_of_next_b_day_date_time.replace(hour=23, minute=0, second=0, microsecond=0)

            credentials_objects = list(CredentialsModel.objects.all())
            nav_free_busy_list = []
            while credentials_objects:
                credentials_object = credentials_objects.pop()
                nav_object = credentials_object.id

                if credentials_object.credential.invalid:
                    credentials_object.delete()
                else:
                    #Obtain valid credential and use it to build authorized service object for given navigator
                    credential = credentials_object.credential
                    http = httplib2.Http()
                    http = credential.authorize(http)
                    service = build("calendar", "v3", http=http)

                    # events_result = service.events().list(calendarId='primary', timeMin=now_date_time,
                    #                                       timeMax=tomorrow_date_time, maxResults=10,
                    #                                       singleEvents=True, orderBy='startTime').execute()
                    # logging.info(events_result)
                    # response_raw_data['Events Lists'].append(events_result)

                    free_busy_args = {"timeMin": earliest_available_date_time.isoformat() + 'Z', # 'Z' indicates UTC time
                                      "timeMax": end_of_next_b_day_date_time.isoformat() + 'Z',
                                      "items": [{"id": "primary"}
                                                ]}
                    free_busy_result = service.freebusy().query(body=free_busy_args).execute()
                    logging.info(free_busy_result)

                    free_busy_entry = [nav_object.return_values_dict(), free_busy_result["calendars"]["primary"]["busy"]]
                    nav_free_busy_list.append(free_busy_entry)

            earliest_available_time = datetime.time(hour=earliest_available_date_time.hour, minute=earliest_available_date_time.minute, second=earliest_available_date_time.second, microsecond=earliest_available_date_time.microsecond)
            start_of_b_day_time = datetime.time(hour=START_OF_BUSINESS_TIMESTAMP.hour, minute=START_OF_BUSINESS_TIMESTAMP.minute, second=START_OF_BUSINESS_TIMESTAMP.second, microsecond=START_OF_BUSINESS_TIMESTAMP.microsecond)
            end_of_b_day_time = datetime.time(hour=END_OF_BUSINESS_TIMESTAMP.hour, minute=END_OF_BUSINESS_TIMESTAMP.minute, second=END_OF_BUSINESS_TIMESTAMP.second, microsecond=END_OF_BUSINESS_TIMESTAMP.microsecond)

            possible_appointment_times = []

            day_1_appointment_timesstamps = bdate_range(start=earliest_available_date_time, end=end_of_next_b_day_date_time, freq='30min', tz=tzutc())
            day_1_appointment_timesstamps = day_1_appointment_timesstamps.tolist()

            for timestamp in day_1_appointment_timesstamps:
                timestamp_time = datetime.time(hour=timestamp.hour, minute=timestamp.minute, second=timestamp.second, microsecond=timestamp.microsecond)
                if earliest_available_time < timestamp_time < end_of_b_day_time:
                    possible_appointment_times.append(timestamp)

            day_2_appointment_timesstamps = bdate_range(start=end_of_next_b_day_date_time, end=end_of_next_b_day_date_time + datetime.timedelta(days=1), freq='30min', tz=tzutc())
            day_2_appointment_timesstamps = day_2_appointment_timesstamps.tolist()

            for timestamp in day_2_appointment_timesstamps:
                timestamp_time = datetime.time(hour=timestamp.hour, minute=timestamp.minute, second=timestamp.second, microsecond=timestamp.microsecond)
                if start_of_b_day_time <= timestamp_time < end_of_b_day_time:
                    possible_appointment_times.append(timestamp)

            for appointment_time in possible_appointment_times:
                response_raw_data["Appointment Times"].append(appointment_time.isoformat()[:-6])

                shuffle(nav_free_busy_list)
                next_available_apt_entry = {"Navigator Name": None,
                                            "Navigator Database ID": None,
                                            "Appointment Date and Time": None,
                                            "Schedule Appointment Link": None,
                                            }
                for nav_free_busy_entry in nav_free_busy_list:
                    nav_info = nav_free_busy_entry[0]
                    nav_busy_list = nav_free_busy_entry[1]
                    if not nav_busy_list:
                        next_available_apt_entry["Navigator Name"] = "{!s} {!s}".format(nav_info["First Name"],nav_info["Last Name"])
                        next_available_apt_entry["Navigator Database ID"] = nav_info["Database ID"]
                        next_available_apt_entry["Appointment Date and Time"] = appointment_time.isoformat()[:-6]
                        next_available_apt_entry["Schedule Appointment Link"] = "http://picbackend.herokuapp.com/v1/scheduleappointment/?navid={!s}".format(str(nav_info["Database ID"]))
                        response_raw_data["Data"]["Next Available Appointments"].append(next_available_apt_entry)
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
                            next_available_apt_entry["Navigator Name"] = "{!s} {!s}".format(nav_info["First Name"],nav_info["Last Name"])
                            next_available_apt_entry["Navigator Database ID"] = nav_info["Database ID"]
                            next_available_apt_entry["Appointment Date and Time"] = appointment_time.isoformat()[:-6]
                            next_available_apt_entry["Schedule Appointment Link"] = "http://picbackend.herokuapp.com/v1/scheduleappointment/?navid={!s}".format(str(nav_info["Database ID"]))
                            response_raw_data["Data"]["Next Available Appointments"].append(next_available_apt_entry)
                            break

    # if a GET request is made, add error message to response data
    else:
        post_errors.append("Request needs POST data")

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response
