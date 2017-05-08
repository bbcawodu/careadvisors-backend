"""
Defines views that handle Patient Innovation Center navigator location based requests
API Version 2
"""


from django.views.generic import View
from django.utils.decorators import method_decorator
from picmodels.models import NavMetricsLocation
from django.views.decorators.csrf import csrf_exempt
from .utils import clean_string_value_from_dict_object
from .utils import add_nav_hub_location
from .utils import modify_nav_hub_location
from .utils import delete_nav_hub_location
from .base import JSONPUTRspMixin
from .base import JSONGETRspMixin


# Need to abstract common variables in get and post class methods into class attributes
class NavHubLocationManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles Patient Innovation Center navigator hub location instance related requests
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(NavHubLocationManagementView, self).dispatch(request, *args, **kwargs)

    def nav_hub_location_management_put_logic(self, post_data, response_raw_data, post_errors):
        # Parse BODY data and add or update navigator hub location entry
        rqst_action = clean_string_value_from_dict_object(post_data, "root", "Database Action", post_errors)

        # if there are no parsing errors, get or create database entries for consumer, location, and point of contact
        # create and save database entry for appointment
        if len(post_errors) == 0 and rqst_action == "Location Addition":
            response_raw_data = add_nav_hub_location(response_raw_data, post_data, post_errors)

        elif len(post_errors) == 0 and rqst_action == "Location Modification":
            response_raw_data = modify_nav_hub_location(response_raw_data, post_data, post_errors)

        elif len(post_errors) == 0 and rqst_action == "Location Deletion":
            response_raw_data = delete_nav_hub_location(response_raw_data, post_data, post_errors)

        return response_raw_data, post_errors

    def nav_hub_location_management_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        # Parse GET params and retreive metrics entries
        nav_location_list = []

        nav_location_entries = NavMetricsLocation.objects.all()
        if 'is_cps_location' in search_params:
            is_cps_location = search_params['is_cps_location']
            nav_location_entries = nav_location_entries.filter(cps_location=is_cps_location)

        for nav_location_entry in nav_location_entries:
            nav_location_list.append(nav_location_entry.return_values_dict())

        if nav_location_list:
            response_raw_data["Data"] = nav_location_list
        else:
            rqst_errors.append("No location entries found in database.")

        return response_raw_data, rqst_errors

    put_logic_function = nav_hub_location_management_put_logic
    get_logic_function = nav_hub_location_management_get_logic
