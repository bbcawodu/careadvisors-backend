"""
Defines views that are responsible for accessing consumer health insurance Related Information
API Version 2
"""

from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
import json
import pokitdok
from django.views.decorators.csrf import csrf_exempt
from picbackend.utils import init_v2_response_data
from picbackend.utils import parse_and_log_errors
from picbackend.utils import fetch_and_parse_pokit_elig_data
from picbackend.utils import build_search_params


@method_decorator(csrf_exempt, name='dispatch')
class ConsumerHealthInsuranceBenefitsView(View):
    def post(self, request, *args, **kwargs):
        """
        Defines view that retrieves consumer health insurance benefits information
        :param request: django request instance object
        :rtype: HttpResponse
        """

        # initialize dictionary for response data, including parsing errors
        response_raw_data, post_errors = init_v2_response_data()

        post_json = request.body.decode('utf-8')
        post_data = json.loads(post_json)

        response_raw_data = fetch_and_parse_pokit_elig_data(post_data, response_raw_data, post_errors)

        response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
        response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
        return response


class TradingPartnerView(View):
    def get(self, request, *args, **kwargs):
        """
        Defines view that retrieves health insurance trading partner information
        :param request: django request instance object
        :rtype: HttpResponse
        """

        # initialize dictionary for response data, including parsing errors
        response_raw_data, rqst_errors = init_v2_response_data()
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
