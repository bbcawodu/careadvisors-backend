from django.views.generic import View

from picbackend.views.utils import JSONGETRspMixin

from picmodels.models import MarketplaceAppointments


# Need to abstract common variables in get and post class methods into class attributes
class MarketplaceAppointmentManagementView(JSONGETRspMixin, View):
    def read_method_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        def retrieve_data_by_primary_params_and_add_to_response():
            data_list = []

            if 'id' in validated_GET_rqst_params:
                rqst_id = validated_GET_rqst_params['id']
                if rqst_id != 'all':
                    list_of_ids = validated_GET_rqst_params['id_list']
                else:
                    list_of_ids = None

                data_list = MarketplaceAppointments.get_serialized_rows_by_id(rqst_id, list_of_ids, rqst_errors)
            elif 'nav_id_list' in validated_GET_rqst_params:
                list_of_nav_ids = validated_GET_rqst_params['nav_id_list']

                data_list = MarketplaceAppointments.get_serialized_rows_by_nav_id(list_of_nav_ids, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response()

    accepted_GET_request_parameters = [
        "nav_id",
        "id"
    ]
    parse_GET_request_and_add_response = read_method_logic
