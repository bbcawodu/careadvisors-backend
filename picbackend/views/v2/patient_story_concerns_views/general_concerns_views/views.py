"""
This module defines views that handle general concerns requests for the Navigator Online Plus patient story conversation
flow
"""

from django.views.generic import View
from django.utils.decorators import method_decorator
from ...utils import clean_string_value_from_dict_object
from picmodels.models import ConsumerGeneralConcern
from .tools import add_general_concern_using_api_rqst_params
from .tools import modify_general_concern_using_api_rqst_params
from .tools import delete_general_concern_using_api_rqst_params
from .tools import retrieve_general_concerns_by_id
from .tools import retrieve_general_concerns_by_name
from django.views.decorators.csrf import csrf_exempt
from ...base import JSONPUTRspMixin
from ...base import JSONGETRspMixin


#Need to abstract common variables in get and post class methods into class attributes
class GeneralConcernsManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles healthcare carrier related requests
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(GeneralConcernsManagementView, self).dispatch(request, *args, **kwargs)

    def general_concerns_management_put_logic(self, post_data, response_raw_data, post_errors):
        # Retrieve database action from post data
        rqst_action = clean_string_value_from_dict_object(post_data, "root", "Database Action", post_errors)

        # If there are no parsing errors, process PUT data based on database action
        if not post_errors:
            if rqst_action == "Concern Addition":
                response_raw_data = add_general_concern_using_api_rqst_params(response_raw_data, post_data, post_errors)
            elif rqst_action == "Concern Modification":
                response_raw_data = modify_general_concern_using_api_rqst_params(response_raw_data, post_data, post_errors)
            elif rqst_action == "Concern Deletion":
                response_raw_data = delete_general_concern_using_api_rqst_params(response_raw_data, post_data, post_errors)
            else:
                post_errors.append("No valid 'Database Action' provided.")

        return response_raw_data, post_errors

    def general_concerns_management_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        general_concerns = ConsumerGeneralConcern.objects.all()

        if 'id' in search_params:
            rqst_carrier_id = search_params['id']
            if rqst_carrier_id != 'all':
                list_of_ids = search_params['id list']
            else:
                list_of_ids = None
            response_raw_data, rqst_errors = retrieve_general_concerns_by_id(response_raw_data, rqst_errors,
                                                                             general_concerns, rqst_carrier_id,
                                                                             list_of_ids)
        elif 'name' in search_params:
            rqst_name = search_params['name']

            response_raw_data, rqst_errors = retrieve_general_concerns_by_name(response_raw_data, rqst_errors,
                                                                               general_concerns, rqst_name)

        return response_raw_data, rqst_errors

    put_logic_function = general_concerns_management_put_logic
    get_logic_function = general_concerns_management_get_logic