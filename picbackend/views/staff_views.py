"""
Defines views that are mapped to url configurations
"""

from django.http import HttpResponse, HttpResponseRedirect
from picmodels.models import PICStaff, CredentialsModel
import json, base64
from django.views.decorators.csrf import csrf_exempt
from picbackend.utils.base import clean_json_string_input, init_response_data, parse_and_log_errors, clean_list_input
from picbackend.utils.db_updates import add_staff, modify_staff, delete_staff, check_or_create_navigator_google_cal
from picbackend.utils.db_queries import retrieve_f_l_name_staff, retrieve_email_staff, retrieve_first_name_staff,\
    retrieve_last_name_staff, retrieve_id_staff, build_search_params, retrieve_county_staff,\
    retrieve_region_staff, retrieve_mpn_staff, get_preferred_nav_apts, get_next_available_nav_apts

from oauth2client.client import flow_from_clientsecrets
from django.conf import settings
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from oauth2client.contrib import xsrfutil
from django.http import HttpResponseBadRequest
import dateutil.parser

FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri=(settings.HOSTURL + '/oauth2callback'))
FLOW.params['access_type'] = 'offline'
FLOW.params["prompt"] = "consent"


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

                check_or_create_navigator_google_cal(credential)

        except PICStaff.DoesNotExist:
            rqst_errors.append('Navigator database entry does not exist for the id: {!s}'.format(str(nav_id)))

    else:
        rqst_errors.append("No valid parameters")

    response_raw_data["Host"] = settings.HOSTURL
    response_raw_data = parse_and_log_errors(response_raw_data, rqst_errors)
    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response


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


@csrf_exempt
def handle_nav_appointments_api_request(request):
    # initialize dictionary for response data, including parsing errors
    response_raw_data, post_errors = init_response_data()

    if request.method == 'POST' or request.is_ajax():
        post_data = request.body.decode('utf-8')
        post_json = json.loads(post_data)

        response_raw_data["Data"] = {}
        response_raw_data["Data"]["Next Available Appointments"] = []
        response_raw_data["Data"]["Preferred Appointments"] = []

        rqst_preferred_times = clean_list_input(post_json, "root", "Preferred Times", post_errors, empty_list_allowed=True)

        valid_rqst_preferred_times_timestamps = []
        for preferred_time_iso_string in rqst_preferred_times:
            if isinstance(preferred_time_iso_string, str):
                try:
                    valid_rqst_preferred_times_timestamps.append(dateutil.parser.parse(preferred_time_iso_string))
                except ValueError:
                    pass

        if valid_rqst_preferred_times_timestamps:
            response_raw_data["Data"]["Preferred Appointments"] = get_preferred_nav_apts(rqst_preferred_times, valid_rqst_preferred_times_timestamps, post_errors)
        else:
            response_raw_data["Data"]["Next Available Appointments"] = get_next_available_nav_apts(post_errors)

    # if a GET request is made, add error message to response data
    else:
        post_errors.append("Request needs POST data")

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
    return response
