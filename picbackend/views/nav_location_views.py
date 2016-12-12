"""
Defines views that are mapped to url configurations
"""

from django.http import HttpResponse
from django.shortcuts import render
from picmodels.models import  NavMetricsLocation
import json
from picbackend.forms import NavMetricsLocationForm
from django.contrib import messages
from django.forms import modelformset_factory
from django.views.decorators.csrf import csrf_exempt
from picbackend.utils.base import clean_json_string_input, init_response_data, parse_and_log_errors
from picbackend.utils.db_updates import add_nav_hub_location, modify_nav_hub_location, delete_nav_hub_location


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
