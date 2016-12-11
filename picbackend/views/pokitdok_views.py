"""
Defines views that are responsible for accessing and supplying Pokitdok data
"""

from django.http import HttpResponse
import json, pokitdok
from django.views.decorators.csrf import csrf_exempt
from picbackend.utils.base import init_response_data, parse_and_log_errors, fetch_and_parse_pokit_elig_data
from picbackend.utils.db_queries import build_search_params


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
