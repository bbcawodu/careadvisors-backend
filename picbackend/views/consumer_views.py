"""
Defines views that are mapped to url configurations
"""

from django.http import HttpResponse
from picmodels.models import PICConsumer
import json
from django.views.decorators.csrf import csrf_exempt
from picbackend.utils.base import clean_json_string_input, init_response_data, parse_and_log_errors
from picbackend.utils.db_updates import add_consumer, modify_consumer, delete_consumer
from picbackend.utils.db_queries import build_search_params, retrieve_f_l_name_consumers,\
    retrieve_email_consumers, retrieve_first_name_consumers, retrieve_last_name_consumers, retrieve_id_consumers,\
    break_results_into_pages


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
