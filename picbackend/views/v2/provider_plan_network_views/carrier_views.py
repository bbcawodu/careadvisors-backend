"""
This module defines views that handle carriers for provider networks contracted with PIC
"""

from django.views.generic import View
from django.utils.decorators import method_decorator
from picbackend.views.v2.utils import clean_string_value_from_dict_object
from picbackend.views.v2.utils import add_carrier
from picbackend.views.v2.utils import modify_carrier
from picbackend.views.v2.utils import delete_carrier
from picbackend.views.v2.utils import retrieve_id_carriers
from picbackend.views.v2.utils import retrieve_name_carriers
from picbackend.views.v2.utils import retrieve_state_carriers
from picmodels.models import HealthcareCarrier
from django.views.decorators.csrf import csrf_exempt
from picbackend.views.v2.base import JSONPUTRspMixin
from picbackend.views.v2.base import JSONGETRspMixin


#Need to abstract common variables in get and post class methods into class attributes
class CarriersManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles healthcare carrier related requests
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CarriersManagementView, self).dispatch(request, *args, **kwargs)

    def carriers_management_put_logic(self, post_data, response_raw_data, post_errors):
        # Retrieve database action from post data
        rqst_action = clean_string_value_from_dict_object(post_data, "root", "Database Action", post_errors)

        # If there are no parsing errors, process PUT data based on database action
        if not post_errors:
            if rqst_action == "Carrier Addition":
                response_raw_data = add_carrier(response_raw_data, post_data, post_errors)
            elif rqst_action == "Carrier Modification":
                response_raw_data = modify_carrier(response_raw_data, post_data, post_errors)
            elif rqst_action == "Carrier Deletion":
                response_raw_data = delete_carrier(response_raw_data, post_data, post_errors)

        return response_raw_data, post_errors

    def carriers_management_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        carriers = HealthcareCarrier.objects.all()

        if 'id' in search_params:
            rqst_carrier_id = search_params['id']
            if rqst_carrier_id != 'all':
                list_of_ids = search_params['id list']
            else:
                list_of_ids = None
            response_raw_data, rqst_errors = retrieve_id_carriers(response_raw_data, rqst_errors, carriers,
                                                                   rqst_carrier_id, list_of_ids)
        elif 'name' in search_params:
            rqst_name = search_params['name']

            response_raw_data, rqst_errors = retrieve_name_carriers(response_raw_data, rqst_errors, carriers, rqst_name)
        elif 'state' in search_params:
            rqst_state = search_params['state']
            list_of_states = search_params['state list']

            response_raw_data, rqst_errors = retrieve_state_carriers(response_raw_data, rqst_errors, carriers,
                                                                     rqst_state, list_of_states)

        return response_raw_data, rqst_errors

    put_logic_function = carriers_management_put_logic
    get_logic_function = carriers_management_get_logic