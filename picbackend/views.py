"""
Defines views that are mapped to url configurations
"""

from django.http import HttpResponse
from django.shortcuts import render
from picmodels.models import PICStaff, MetricsSubmission, PICConsumer, PlanStat
import json, sys, pokitdok
from django.views.decorators.csrf import csrf_exempt
from picbackend.utils.base import clean_json_string_input, init_response_data, parse_and_log_errors, fetch_and_parse_pokit_elig_data
from picbackend.utils.db_updates import add_staff, modify_staff, delete_staff, add_consumer, modify_consumer, delete_consumer,\
    add_or_update_metrics_entity
from picbackend.utils.db_queries import retrieve_f_l_name_staff, retrieve_email_staff, retrieve_first_name_staff,\
    retrieve_last_name_staff, retrieve_id_staff, build_search_params, retrieve_f_l_name_consumers,\
    retrieve_email_consumers, retrieve_first_name_consumers, retrieve_last_name_consumers, retrieve_id_consumers,\
    break_results_into_pages, group_metrics, retrieve_id_metrics, retrieve_f_l_name_metrics,\
    retrieve_first_name_metrics, retrieve_last_name_metrics, retrieve_email_metrics, retrieve_county_staff,\
    retrieve_region_staff


# defines view for home page
def index(request):
    return render(request, "home_page.html")


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


# defines view for saving scheduled appointments to the database
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

    # Start with this query for all and then evaluate down from request params
    # Queries arent evaluated until you read the data
    metrics_submissions = MetricsSubmission.objects.all()
    if 'zipcode list' in search_params:
        list_of_zipcodes = search_params['zipcode list']
        metrics_submissions = metrics_submissions.filter(zipcode__in=list_of_zipcodes)
    if 'look up date' in search_params:
        look_up_date = search_params['look up date']
        metrics_submissions = metrics_submissions.filter(submission_date__gte=look_up_date)
    if 'start date' in search_params:
        rqst_start_date = search_params['start date']
        metrics_submissions = metrics_submissions.filter(submission_date__gte=rqst_start_date)
    if 'end date' in search_params:
        rqst_end_date = search_params['end date']
        metrics_submissions = metrics_submissions.filter(submission_date__lte=rqst_end_date)

    if 'id' in search_params:
        rqst_staff_id = search_params['id']
        if rqst_staff_id != 'all':
            list_of_ids = search_params['id list']
        else:
            list_of_ids = None
        metrics_dict = retrieve_id_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_staff_id,
                                           list_of_ids)
    elif 'first name' in search_params and 'last name' in search_params:
        rqst_fname = search_params['first name']
        rqst_lname = search_params['last name']
        list_of_first_names = search_params['first name list']
        list_of_last_names = search_params['last name list']
        metrics_dict = retrieve_f_l_name_metrics(response_raw_data, rqst_errors, metrics_submissions,
                                                 list_of_first_names, list_of_last_names, rqst_fname, rqst_lname)
    elif 'first name' in search_params:
        rqst_fname = search_params['first name']
        list_of_first_names = search_params['first name list']
        metrics_dict = retrieve_first_name_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_fname,
                                                   list_of_first_names)
    elif 'last name' in search_params:
        rqst_lname = search_params['last name']
        list_of_last_names = search_params['last name list']
        metrics_dict = retrieve_last_name_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_lname,
                                                  list_of_last_names)
    elif 'email' in search_params:
        rqst_staff_email = search_params['email']
        list_of_emails = search_params['email list']
        metrics_dict = retrieve_email_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_staff_email,
                                              list_of_emails)

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
