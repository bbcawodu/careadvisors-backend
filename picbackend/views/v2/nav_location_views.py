"""
Defines views that handle Patient Innovation Center navigator location based requests
API Version 2
"""

from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from picmodels.models import NavMetricsLocation
import json
from django.views.decorators.csrf import csrf_exempt
from .utils import clean_json_string_input
from .utils import init_v2_response_data
from .utils import parse_and_log_errors
from .utils import add_nav_hub_location
from .utils import modify_nav_hub_location
from .utils import delete_nav_hub_location


#Need to abstract common variables in get and post class methods into class attributes
@method_decorator(csrf_exempt, name='dispatch')
class NavHubLocationManagementView(View):
    def put(self, request, *args, **kwargs):
        """
        Defines view that handles Patient Innovation Center navigator hub location instance edit requests
        :param request: django request instance object
        :rtype: HttpResponse
        """

        # initialize dictionary for response data, including parsing errors
        response_raw_data, post_errors = init_v2_response_data()

        post_json = request.body.decode('utf-8')
        post_data = json.loads(post_json)

        # Code to parse POSTed json request
        rqst_action = clean_json_string_input(post_json, "root", "Database Action", post_errors)

        # if there are no parsing errors, get or create database entries for consumer, location, and point of contact
        # create and save database entry for appointment
        if len(post_errors) == 0 and rqst_action == "Location Addition":
            response_raw_data = add_nav_hub_location(response_raw_data, post_data, post_errors)

        elif len(post_errors) == 0 and rqst_action == "Location Modification":
            response_raw_data = modify_nav_hub_location(response_raw_data, post_data, post_errors)

        elif len(post_errors) == 0 and rqst_action == "Location Deletion":
            response_raw_data = delete_nav_hub_location(response_raw_data, post_data, post_errors)

        response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
        response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
        return response

    def get(self, request, *args, **kwargs):
        """
        Defines view that handles Patient Innovation Center navigator hub location instance retrieval requests
        :param request: django request instance object
        :rtype: HttpResponse
        """

        response_raw_data, rqst_errors = init_v2_response_data()
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
