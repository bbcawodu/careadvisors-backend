"""
This module defines views that handle accepted plans for provider networks contracted with PIC
"""

from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from picmodels.models import HealthcarePlan
from ...utils import clean_string_value_from_dict_object
from ...base import JSONPUTRspMixin
from ...base import JSONGETRspMixin
from .tools import add_plan
from .tools import modify_plan
from .tools import delete_plan
from .tools import retrieve_id_plans
from .tools import retrieve_name_plans
from .tools import retrieve_plans_by_carrier_id
from .tools import retrieve_plans_by_carrier_state
from .tools import retrieve_plans_by_carrier_name
from .tools import retrieve_plans_by_accepted_location_id


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
        include_summary_report = [False]
        include_detailed_report = [False]

        def filter_db_objects_by_secondary_params(search_params, db_objects):
            if 'include_summary_report' in search_params:
                include_summary_report[0] = search_params['include_summary_report']
            if 'include_detailed_report' in search_params:
                include_detailed_report[0] = search_params['include_detailed_report']
            return db_objects

        plans = filter_db_objects_by_secondary_params(search_params, plans)

        if 'id' in search_params:
            rqst_plan_id = search_params['id']
            if rqst_plan_id != 'all':
                list_of_ids = search_params['id list']
            else:
                list_of_ids = None
            response_raw_data, rqst_errors = retrieve_id_plans(response_raw_data, rqst_errors, plans,
                                                                   rqst_plan_id, list_of_ids, include_summary_report=include_summary_report[0], include_detailed_report=include_detailed_report[0])
        elif 'name' in search_params:
            rqst_name = search_params['name']

            response_raw_data, rqst_errors = retrieve_name_plans(response_raw_data, rqst_errors, plans, rqst_name, include_summary_report=include_summary_report[0], include_detailed_report=include_detailed_report[0])
        elif 'carrier state' in search_params:
            rqst_carrier_state = search_params['carrier state']
            list_of_carrier_states = search_params['carrier state list']

            response_raw_data, rqst_errors = retrieve_plans_by_carrier_state(response_raw_data, rqst_errors, plans,
                                                                             rqst_carrier_state, list_of_carrier_states, include_summary_report=include_summary_report[0], include_detailed_report=include_detailed_report[0])
        elif 'carrier name' in search_params:
            rqst_carrier_name = search_params['carrier name']

            response_raw_data, rqst_errors = retrieve_plans_by_carrier_name(response_raw_data, rqst_errors, plans,
                                                                            rqst_carrier_name, include_summary_report=include_summary_report[0], include_detailed_report=include_detailed_report[0])
        elif 'carrier id' in search_params:
            rqst_carrier_id = search_params['carrier id']
            list_of_carrier_ids = search_params['carrier id list']

            response_raw_data, rqst_errors = retrieve_plans_by_carrier_id(response_raw_data, rqst_errors, plans,
                                                                          rqst_carrier_id, list_of_carrier_ids, include_summary_report=include_summary_report[0], include_detailed_report=include_detailed_report[0])
        elif 'accepted_location_id' in search_params:
            rqst_accepted_location_id = search_params['accepted_location_id']
            list_of_accepted_location_ids = search_params['accepted_location_id_list']

            response_raw_data, rqst_errors = retrieve_plans_by_accepted_location_id(response_raw_data, rqst_errors,
                                                                                    plans, rqst_accepted_location_id,
                                                                                    list_of_accepted_location_ids, include_summary_report=include_summary_report[0], include_detailed_report=include_detailed_report[0])

        return response_raw_data, rqst_errors

    put_logic_function = plans_management_put_logic
    get_logic_function = plans_management_get_logic