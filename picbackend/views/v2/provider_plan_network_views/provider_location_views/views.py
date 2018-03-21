"""
This module defines views that handle hospital/provider locations for provider networks contracted with PIC
"""

from django.views.generic import View

from picbackend.views.utils import JSONGETRspMixin
from picbackend.views.utils import JSONPUTRspMixin

from picmodels.models import ProviderLocation

from .tools import validate_put_rqst_params


# Need to abstract common variables in get and post class methods into class attributes
class ProviderLocationsManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    def provider_locations_management_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        validated_put_rqst_params = validate_put_rqst_params(rqst_body, rqst_errors)
        rqst_action = validated_put_rqst_params['rqst_action']

        if not rqst_errors:
            provider_location_obj = None

            if rqst_action == "create":
                provider_location_obj = ProviderLocation.create_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )
            elif rqst_action == "update":
                provider_location_obj = ProviderLocation.update_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )
            elif rqst_action == "delete":
                ProviderLocation.delete_row_w_validated_params(validated_put_rqst_params, rqst_errors)

                if not rqst_errors:
                    response_raw_data['Data']["row"] = "Deleted"
            else:
                rqst_errors.append("No valid 'db_action' provided.")

            if provider_location_obj:
                response_raw_data['Data']["row"] = provider_location_obj.return_values_dict()

    def provider_locations_management_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        def retrieve_data_by_primary_params_and_add_to_response():
            data_list = []

            if 'id' in validated_GET_rqst_params:
                data_list = ProviderLocation.get_serialized_rows_by_id(
                    validated_GET_rqst_params,
                    rqst_errors
                )
            elif 'name' in validated_GET_rqst_params:
                data_list = ProviderLocation.get_serialized_rows_by_name(validated_GET_rqst_params, rqst_errors)
            elif 'network_name' in validated_GET_rqst_params:
                data_list = ProviderLocation.get_serialized_rows_by_network_name(validated_GET_rqst_params, rqst_errors)
            elif 'network_id' in validated_GET_rqst_params:
                data_list = ProviderLocation.get_serialized_rows_by_network_id(validated_GET_rqst_params, rqst_errors)
            elif 'state' in validated_GET_rqst_params:
                data_list = ProviderLocation.get_serialized_rows_by_state(validated_GET_rqst_params, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response()

    parse_PUT_request_and_add_response = provider_locations_management_put_logic

    accepted_GET_request_parameters = [
        "id",
        "name",
        "network_name",
        'state',
        "network_id"
    ]
    parse_GET_request_and_add_response = provider_locations_management_get_logic
