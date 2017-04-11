"""
This module defines views that handle carriers, accepted plans, and hospital/provider locations for provider networks
contracted with PIC
"""

from django.views.generic import View
from django.utils.decorators import method_decorator
from .utils import clean_string_value_from_dict_object
from .utils import add_carrier
from .utils import modify_carrier
from .utils import delete_carrier
from django.views.decorators.csrf import csrf_exempt
from .base import JSONPUTRspMixin
from .base import JSONGETRspMixin


#Need to abstract common variables in get and post class methods into class attributes
class CarriersManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles Patient Innovation Center metrics instance related requests
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

        return response_raw_data, rqst_errors

    put_logic_function = carriers_management_put_logic
    get_logic_function = carriers_management_get_logic
