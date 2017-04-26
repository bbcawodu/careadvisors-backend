"""
This module defines views that handle accepted plans for provider networks contracted with PIC
"""

from django.views.generic import View
from django.utils.decorators import method_decorator
from picbackend.views.v2.utils import clean_string_value_from_dict_object
from picbackend.views.v2.utils import add_plan
from picbackend.views.v2.utils import modify_plan
from picbackend.views.v2.utils import delete_plan
from picbackend.views.v2.utils import retrieve_id_plans
from picbackend.views.v2.utils import retrieve_name_plans
from picbackend.views.v2.utils import retrieve_plans_by_carrier_id
from picbackend.views.v2.utils import retrieve_plans_by_carrier_state
from picbackend.views.v2.utils import retrieve_plans_by_carrier_name
from picbackend.views.v2.utils import retrieve_plans_by_accepted_location_id
from picmodels.models import HealthcarePlan
from django.views.decorators.csrf import csrf_exempt
from picbackend.views.v2.base import JSONPUTRspMixin
from picbackend.views.v2.base import JSONGETRspMixin


#Need to abstract common variables in get and post class methods into class attributes
class PlansManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles healthcare carrier related requests
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PlansManagementView, self).dispatch(request, *args, **kwargs)

    def plans_management_put_logic(self, post_data, response_raw_data, post_errors):
        # Retrieve database action from post data
        rqst_action = clean_string_value_from_dict_object(post_data, "root", "Database Action", post_errors)

        # If there are no parsing errors, process PUT data based on database action
        if not post_errors:
            if rqst_action == "Plan Addition":
                response_raw_data = add_plan(response_raw_data, post_data, post_errors)
            elif rqst_action == "Plan Modification":
                response_raw_data = modify_plan(response_raw_data, post_data, post_errors)
            elif rqst_action == "Plan Deletion":
                response_raw_data = delete_plan(response_raw_data, post_data, post_errors)

        return response_raw_data, post_errors

    def plans_management_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        plans = HealthcarePlan.objects.all()

        if 'id' in search_params:
            rqst_plan_id = search_params['id']
            if rqst_plan_id != 'all':
                list_of_ids = search_params['id list']
            else:
                list_of_ids = None
            response_raw_data, rqst_errors = retrieve_id_plans(response_raw_data, rqst_errors, plans,
                                                                   rqst_plan_id, list_of_ids)
        elif 'name' in search_params:
            rqst_name = search_params['name']

            response_raw_data, rqst_errors = retrieve_name_plans(response_raw_data, rqst_errors, plans, rqst_name)
        elif 'carrier state' in search_params:
            rqst_carrier_state = search_params['carrier state']
            list_of_carrier_states = search_params['carrier state list']

            response_raw_data, rqst_errors = retrieve_plans_by_carrier_state(response_raw_data, rqst_errors, plans,
                                                                             rqst_carrier_state, list_of_carrier_states)
        elif 'carrier name' in search_params:
            rqst_carrier_name = search_params['carrier name']

            response_raw_data, rqst_errors = retrieve_plans_by_carrier_name(response_raw_data, rqst_errors, plans,
                                                                            rqst_carrier_name)
        elif 'carrier id' in search_params:
            rqst_carrier_id = search_params['carrier id']
            list_of_carrier_ids = search_params['carrier id list']

            response_raw_data, rqst_errors = retrieve_plans_by_carrier_id(response_raw_data, rqst_errors, plans,
                                                                          rqst_carrier_id, list_of_carrier_ids)
        elif 'accepted_location_id' in search_params:
            rqst_accepted_location_id = search_params['accepted_location_id']
            list_of_accepted_location_ids = search_params['accepted_location_id_list']

            response_raw_data, rqst_errors = retrieve_plans_by_accepted_location_id(response_raw_data, rqst_errors,
                                                                                    plans, rqst_accepted_location_id,
                                                                                    list_of_accepted_location_ids)

        return response_raw_data, rqst_errors

    put_logic_function = plans_management_put_logic
    get_logic_function = plans_management_get_logic