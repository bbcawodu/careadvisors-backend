"""
Defines views that are responsible for accessing consumer health insurance Related Information
API Version 2
"""

import pokitdok
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .tools import fetch_and_parse_pokit_elig_data
from ..base import JSONPOSTRspMixin
from ..base import JSONGETRspMixin


class ConsumerHealthInsuranceBenefitsView(JSONPOSTRspMixin, View):
    """
    Defines view that retrieves consumer health insurance benefits information
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ConsumerHealthInsuranceBenefitsView, self).dispatch(request, *args, **kwargs)

    def insurance_benefits_logic(self, post_data, response_raw_data, post_errors):
        # Fetch eligibility data from Pokitdok
        raw_elig_data, parsed_elig_data = fetch_and_parse_pokit_elig_data(post_data, post_errors)

        response_raw_data['raw_eligibility_data'] = raw_elig_data
        response_raw_data['Data'] = parsed_elig_data

    post_logic_function = insurance_benefits_logic


class TradingPartnerView(JSONGETRspMixin, View):
    """
    Defines view that retrieves health insurance trading partner information
    """

    def trading_partner_logic(self, request, search_params, response_raw_data, rqst_errors):
        def retrieve_data_by_primary_params_and_add_to_response():
            # create Pokitdok API object
            pd = pokitdok.api.connect('fbSgQ0sM3xQNI5m8TyxR', 'du6JkRfNcHt8wNashtpf7Mdr96thZyn8Kilo9xoB')

            # make request to pokitdok
            if "partnerid" in search_params:
                trading_partners = pd.trading_partners(search_params["partnerid"])
            else:
                trading_partners = pd.trading_partners()

            response_raw_data["Data"] = trading_partners["data"]

        retrieve_data_by_primary_params_and_add_to_response()

    get_logic_function = trading_partner_logic
