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
from .utils import retrieve_id_carriers
from .utils import retrieve_name_carriers
from .utils import retrieve_state_carriers
from .utils import add_plan
from .utils import modify_plan
from .utils import delete_plan
from .utils import retrieve_id_plans
from .utils import retrieve_name_plans
from .utils import retrieve_plans_by_carrier_id
from .utils import retrieve_plans_by_carrier_state
from .utils import retrieve_plans_by_carrier_name
from .utils import add_provider_network
from .utils import modify_provider_network
from .utils import delete_provider_network
from .utils import retrieve_provider_networks_by_id
from .utils import retrieve_provider_networks_by_name
from picmodels.models import HealthcareCarrier
from picmodels.models import HealthcarePlan
from picmodels.models import ProviderLocation
from picmodels.models import ProviderNetwork
from django.views.decorators.csrf import csrf_exempt
from .base import JSONPUTRspMixin
from .base import JSONGETRspMixin


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

        return response_raw_data, rqst_errors

    put_logic_function = plans_management_put_logic
    get_logic_function = plans_management_get_logic


#Need to abstract common variables in get and post class methods into class attributes
class ProviderLocationsManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles healthcare carrier related requests
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ProviderLocationsManagementView, self).dispatch(request, *args, **kwargs)

    def provider_locations_management_put_logic(self, post_data, response_raw_data, post_errors):
        # Retrieve database action from post data
        rqst_action = clean_string_value_from_dict_object(post_data, "root", "Database Action", post_errors)

        # If there are no parsing errors, process PUT data based on database action
        if not post_errors:
            if rqst_action == "Provider Location Addition":
                response_raw_data = add_plan(response_raw_data, post_data, post_errors)
            elif rqst_action == "Provider Location Modification":
                response_raw_data = modify_plan(response_raw_data, post_data, post_errors)
            elif rqst_action == "Provider Location Deletion":
                response_raw_data = delete_plan(response_raw_data, post_data, post_errors)

        return response_raw_data, post_errors

    def provider_locations_management_get_logic(self, request, search_params, response_raw_data, rqst_errors):
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

        return response_raw_data, rqst_errors

    put_logic_function = provider_locations_management_put_logic
    get_logic_function = provider_locations_management_get_logic


#Need to abstract common variables in get and post class methods into class attributes
class ProviderNetworksManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles healthcare carrier related requests
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ProviderNetworksManagementView, self).dispatch(request, *args, **kwargs)

    def provider_networks_management_put_logic(self, post_data, response_raw_data, post_errors):
        # Retrieve database action from post data
        rqst_action = clean_string_value_from_dict_object(post_data, "root", "Database Action", post_errors)

        # If there are no parsing errors, process PUT data based on database action
        if not post_errors:
            if rqst_action == "Provider Network Addition":
                response_raw_data = add_provider_network(response_raw_data, post_data, post_errors)
            elif rqst_action == "Provider Network Modification":
                response_raw_data = modify_provider_network(response_raw_data, post_data, post_errors)
            elif rqst_action == "Provider Network Deletion":
                response_raw_data = delete_provider_network(response_raw_data, post_data, post_errors)

        return response_raw_data, post_errors

    def provider_networks_management_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        provider_networks = ProviderNetwork.objects.all()

        if 'id' in search_params:
            rqst_provider_network_id = search_params['id']
            if rqst_provider_network_id != 'all':
                list_of_ids = search_params['id list']
            else:
                list_of_ids = None
            response_raw_data, rqst_errors = retrieve_provider_networks_by_id(response_raw_data, rqst_errors,
                                                                              provider_networks, rqst_provider_network_id,
                                                                              list_of_ids)
        elif 'name' in search_params:
            rqst_name = search_params['name']

            response_raw_data, rqst_errors = retrieve_provider_networks_by_name(response_raw_data, rqst_errors,
                                                                                provider_networks, rqst_name)

        return response_raw_data, rqst_errors

    put_logic_function = provider_networks_management_put_logic
    get_logic_function = provider_networks_management_get_logic
