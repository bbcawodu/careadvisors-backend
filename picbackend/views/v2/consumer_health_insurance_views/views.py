import pokitdok
from django.views.generic import View

from picbackend.views.utils import JSONGETRspMixin
from picbackend.views.utils import JSONPOSTRspMixin
from .tools import fetch_and_parse_pokit_elig_data


class ConsumerHealthInsuranceBenefitsView(JSONPOSTRspMixin, JSONGETRspMixin, View):
    def insurance_benefits_logic(self, rqst_body, response_raw_data, rqst_errors):
        # Fetch eligibility data from Pokitdok
        raw_elig_data, parsed_elig_data = fetch_and_parse_pokit_elig_data(rqst_body, rqst_errors)

        response_raw_data['raw_eligibility_data'] = raw_elig_data
        response_raw_data['Data'] = parsed_elig_data

    def consumer_health_insurance_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        pass

    parse_POST_request_and_add_response = insurance_benefits_logic

    accepted_GET_request_parameters = [

    ]
    parse_GET_request_and_add_response = consumer_health_insurance_get_logic


class TradingPartnerView(JSONGETRspMixin, View):
    def trading_partner_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        def retrieve_data_by_primary_params_and_add_to_response():
            # create Pokitdok API object
            pd = pokitdok.api.connect('fbSgQ0sM3xQNI5m8TyxR', 'du6JkRfNcHt8wNashtpf7Mdr96thZyn8Kilo9xoB')

            # make request to pokitdok
            if "partner_id" in validated_GET_rqst_params:
                trading_partners = pd.trading_partners(validated_GET_rqst_params["partner_id"])
            else:
                trading_partners = pd.trading_partners()

            response_raw_data["Data"] = trading_partners["data"]

        retrieve_data_by_primary_params_and_add_to_response()

    parse_GET_request_and_add_response = trading_partner_logic
    accepted_GET_request_parameters = ["partner_id"]
