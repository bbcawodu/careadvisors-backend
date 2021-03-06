"""
Defines views that handle Patient Assist Appointment Scheduler related views
API Version 2
"""

import dateutil.parser
import json
import base64
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.conf import settings
from django.views.generic import View
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from picbackend.views.utils import JSONPUTRspMixin
from picbackend.views.utils import JSONGETRspMixin
from picbackend.views.utils import JSONPOSTRspMixin
from picbackend.views.utils import JSONDELETERspMixin
from picmodels.models import Navigators
from picmodels.models import CredentialsModel
from picbackend.views.utils import init_v2_response_data
from picbackend.views.utils import parse_and_log_errors
from picbackend.views.utils import clean_list_value_from_dict_object
from picbackend.views.utils import validate_get_request_parameters
from .tools import check_or_create_navigator_google_cal
from .tools import add_nav_apt_to_google_calendar
from .tools import delete_nav_apt_from_google_calendar
from .tools import get_preferred_nav_apts
from .tools import get_next_available_nav_apts
from .tools import get_nav_scheduled_appointments


FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri=(settings.HOSTURL + '/v2/oauth2callback'))
FLOW.params['access_type'] = 'offline'
FLOW.params["prompt"] = "consent"


class NavGoogleCalendarAccessRequestView(View):
    def get(self, request, *args, **kwargs):
        """
        Defines view that requests authorization for Patient Innovation Center to access a given navigator's Google
        calendar

        :param request: django request instance object
        :rtype: HttpResponse
        """

        response_raw_data, rqst_errors = init_v2_response_data()
        search_params = validate_get_request_parameters(request.GET, ["nav_id"], rqst_errors)

        if 'nav_id' in search_params:
            nav_id = search_params["nav_id"]
            try:
                picstaff_object = Navigators.objects.get(id=nav_id)
                storage = DjangoORMStorage(CredentialsModel, 'id', nav_id, 'credential')
                credential = storage.get()
                if credential is None or credential.invalid == True:
                    google_token = xsrfutil.generate_token(settings.SECRET_KEY, picstaff_object.id)
                    params_dict = {"nav_id": nav_id,
                                   "token": google_token.decode('ascii')}
                    params_json = json.dumps(params_dict).encode('ascii')
                    params_base64_encoded = base64.urlsafe_b64encode(params_json)
                    authorize_url = FLOW.step1_get_authorize_url(state=params_base64_encoded)
                    return HttpResponseRedirect(authorize_url)

                else:
                    response_raw_data["Data"] = "Authorized!"

                    check_or_create_navigator_google_cal(credential, rqst_errors)

            except Navigators.DoesNotExist:
                rqst_errors.append('Navigator database entry does not exist for the id: {!s}'.format(str(nav_id)))

        else:
            rqst_errors.append("No valid parameters")

        response_raw_data["Host"] = settings.HOSTURL
        parse_and_log_errors(response_raw_data, rqst_errors)
        response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
        return response


class GoogleCalendarAuthReturnView(View):
    def get(self, request, *args, **kwargs):
        """
        Defines view that handles redirect information from Google when authorizing access to a given navigator's
        Google Calendar

        :param request: django request instance object
        :rtype: HttpResponse
        """

        state_string = request.GET['state']
        state_dict = json.loads(base64.urlsafe_b64decode(state_string).decode('ascii'))
        if not xsrfutil.validate_token(settings.SECRET_KEY, bytes(state_dict['token'], 'utf-8'), state_dict["nav_id"]):
            return HttpResponseBadRequest()
        # if not xsrfutil.validate_token(SECRET_KEY, bytes(request.GET['state'], 'utf-8'), search_params["nav_id"]):
        #     return HttpResponseBadRequest()
        credential = FLOW.step2_exchange(request.REQUEST)
        storage = DjangoORMStorage(CredentialsModel, 'id', Navigators.objects.get(id=state_dict["nav_id"]), 'credential')
        storage.put(credential)
        return HttpResponseRedirect("/v2/calendar_auth/?nav_id={!s}".format(state_dict["nav_id"]))


# Need to abstract common variables in get and post class methods into class attributes
class PatientAssistAptMgtView(JSONGETRspMixin, JSONPOSTRspMixin, JSONPUTRspMixin, JSONDELETERspMixin, View):
    """
    Defines views that manage scheduled consumer appointments for the Patient Assist Plugin
    """

    def nav_scheduled_appointments_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        response_raw_data["Data"] = {"Scheduled Appointments": None}

        if 'nav_id' in validated_GET_rqst_params and not rqst_errors:
            nav_id = validated_GET_rqst_params["nav_id"]

            try:
                picstaff_object = Navigators.objects.get(id=nav_id)
                credentials_object = CredentialsModel.objects.get(id=picstaff_object)
                nav_info = picstaff_object.return_values_dict()
                response_raw_data["Data"]["Scheduled Appointments"] = get_nav_scheduled_appointments(nav_info,
                                                                                                     credentials_object,
                                                                                                     rqst_errors)

            except Navigators.DoesNotExist:
                rqst_errors.append('Navigator database entry does not exist for the id: {!s}'.format(str(nav_id)))
            except CredentialsModel.DoesNotExist:
                rqst_errors.append('Google Credentials database entry does not exist for the navigator with id: {!s}'.format(str(nav_id)))

        else:
            rqst_errors.append("No valid parameters")

        response_raw_data["Host"] = settings.HOSTURL

    def available_nav_appointments_logic(self, rqst_body, response_raw_data, rqst_errors):
        response_raw_data["Data"] = {}
        response_raw_data["Data"]["Next Available Appointments"] = []
        response_raw_data["Data"]["Preferred Appointments"] = []

        rqst_preferred_times = clean_list_value_from_dict_object(rqst_body, "root", "Preferred Times", rqst_errors, empty_list_allowed=True)

        valid_rqst_preferred_times_timestamps = []
        for preferred_time_iso_string in rqst_preferred_times:
            if isinstance(preferred_time_iso_string, str):
                try:
                    valid_rqst_preferred_times_timestamps.append(dateutil.parser.parse(preferred_time_iso_string))
                except ValueError:
                    pass

        if valid_rqst_preferred_times_timestamps:
            response_raw_data["Data"]["Preferred Appointments"] = get_preferred_nav_apts(rqst_preferred_times, valid_rqst_preferred_times_timestamps, rqst_errors)
        else:
            response_raw_data["Data"]["Next Available Appointments"] = get_next_available_nav_apts(rqst_errors)

    def add_nav_scheduled_appointment_logic(self, rqst_body, response_raw_data, rqst_errors):
        response_raw_data["Data"] = {"Confirmed Appointment": None,
                                     "Consumer ID": None}

        confirmed_appointment, consumer_dict = add_nav_apt_to_google_calendar(rqst_body, rqst_errors)
        response_raw_data["Data"]["Confirmed Appointment"] = confirmed_appointment
        if consumer_dict:
            response_raw_data["Data"]["Consumer ID"] = consumer_dict["Database ID"]

    def delete_nav_scheduled_appointment_logic(self, rqst_body, response_raw_data, rqst_errors):
        response_raw_data["Data"] = {"Deleted Appointment": False}

        response_raw_data["Data"]["Deleted Appointment"] = delete_nav_apt_from_google_calendar(rqst_body, rqst_errors)

    parse_PUT_request_and_add_response = add_nav_scheduled_appointment_logic
    parse_POST_request_and_add_response = available_nav_appointments_logic
    parse_DELETE_request_and_add_response = delete_nav_scheduled_appointment_logic

    accepted_GET_request_parameters = [
        "nav_id"
    ]
    parse_GET_request_and_add_response = nav_scheduled_appointments_logic
