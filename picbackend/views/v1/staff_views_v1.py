"""
Defines views that handle Patient Innovation Center Staff based requests
API Version 1
"""

from django.http import HttpResponse
from picmodels.models import PICStaff
import json
from django.views.decorators.csrf import csrf_exempt
from picbackend.utils import clean_json_string_input
from picbackend.utils import init_response_data
from picbackend.utils import parse_and_log_errors
from picbackend.utils import build_search_params
from picbackend.utils import add_staff
from picbackend.utils import modify_staff
from picbackend.utils import delete_staff
from picbackend.utils import retrieve_f_l_name_staff
from picbackend.utils import retrieve_email_staff
from picbackend.utils import retrieve_first_name_staff
from picbackend.utils import retrieve_last_name_staff
from picbackend.utils import retrieve_id_staff
from picbackend.utils import retrieve_mpn_staff
from picbackend.utils import retrieve_county_staff
from picbackend.utils import retrieve_region_staff


@csrf_exempt
def handle_staff_edit_request(request):
    """
    Defines view that handles Patient Innovation Center staff instance edit requests
    :param request: django request instance object
    :rtype: HttpResponse
    """

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


# defines view for returning staff data from api requests
def handle_staff_api_request(request):
    """
    Defines view that handles Patient Innovation Center staff instance retrieval requests
    :param request: django request instance object
    :rtype: HttpResponse
    """

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
