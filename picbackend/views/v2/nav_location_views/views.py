from django.views.generic import View

from picbackend.views.utils import JSONGETRspMixin
from picbackend.views.utils import JSONPUTRspMixin

from picmodels.models import NavMetricsLocation

from .tools import validate_put_rqst_params


# Need to abstract common variables in get and post class methods into class attributes
class NavHubLocationManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles Patient Innovation Center navigator hub location instance related requests
    """

    def nav_hub_location_management_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        validated_put_rqst_params = validate_put_rqst_params(rqst_body, rqst_errors)
        rqst_action = validated_put_rqst_params['rqst_action']

        if not rqst_errors:
            if rqst_action == "create":
                location_instance = NavMetricsLocation.create_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )

                if location_instance:
                    response_raw_data['Data']["row"] = location_instance.return_values_dict()
            elif rqst_action == "update":
                location_instance = NavMetricsLocation.update_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )

                if location_instance:
                    response_raw_data['Data']["row"] = location_instance.return_values_dict()
            elif rqst_action == "delete":
                NavMetricsLocation.delete_row_w_validated_params(validated_put_rqst_params, rqst_errors)

                if not rqst_errors:
                    response_raw_data['Data']["row"] = "Deleted"
            else:
                rqst_errors.append("No valid 'db_action' provided.")

    def nav_hub_location_management_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        def retrieve_data_and_add_to_response():
            if 'id' in validated_GET_rqst_params:
                rqst_nav_hub_location_id = validated_GET_rqst_params['id']
                if rqst_nav_hub_location_id != 'all':
                    list_of_ids = validated_GET_rqst_params['id_list']
                else:
                    list_of_ids = None
            else:
                rqst_nav_hub_location_id = 'all'
                list_of_ids = None

            data_list = NavMetricsLocation.retrieve_nav_hub_location_data_by_id(
                validated_GET_rqst_params,
                rqst_nav_hub_location_id,
                list_of_ids,
                rqst_errors
            )

            response_raw_data["Data"] = data_list

        retrieve_data_and_add_to_response()

    parse_PUT_request_and_add_response = nav_hub_location_management_put_logic

    accepted_GET_request_parameters = [
        "is_cps_location",
        "id"
    ]
    parse_GET_request_and_add_response = nav_hub_location_management_get_logic
