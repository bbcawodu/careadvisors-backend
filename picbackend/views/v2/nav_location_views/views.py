"""
Defines views that handle Patient Innovation Center navigator location based requests
API Version 2
"""


from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from picmodels.models import NavMetricsLocation
from ..base import JSONPUTRspMixin
from ..base import JSONGETRspMixin
from ..utils import clean_string_value_from_dict_object
from .tools import validate_rqst_params_and_add_instance
from .tools import validate_rqst_params_and_modify_instance
from .tools import validate_rqst_params_and_delete_instance
from .tools import retrieve_nav_hub_location_data_by_id


# Need to abstract common variables in get and post class methods into class attributes
class NavHubLocationManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles Patient Innovation Center navigator hub location instance related requests
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(NavHubLocationManagementView, self).dispatch(request, *args, **kwargs)

    def nav_hub_location_management_put_logic(self, post_data, response_raw_data, post_errors):
        rqst_action = clean_string_value_from_dict_object(post_data, "root", "Database Action", post_errors)

        if not post_errors:
            if rqst_action == "Location Addition":
                location_instance = validate_rqst_params_and_add_instance(post_data, post_errors)

                if location_instance:
                    response_raw_data['Data'] = {"Database ID": location_instance.id}
            elif rqst_action == "Location Modification":
                location_instance = validate_rqst_params_and_modify_instance(post_data, post_errors)

                if location_instance:
                    response_raw_data['Data'] = {"Database ID": location_instance.id}
            elif rqst_action == "Location Deletion":
                validate_rqst_params_and_delete_instance(post_data, post_errors)

                if not post_errors:
                    response_raw_data['Data']["Database ID"] = "Deleted"
            else:
                post_errors.append("No valid 'Database Action' provided.")

    def nav_hub_location_management_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        nav_hub_location_qset = NavMetricsLocation.objects.all()

        def filter_db_objects_by_secondary_params(db_objects):
            if 'is_cps_location' in search_params:
                is_cps_location = search_params['is_cps_location']
                db_objects = db_objects.filter(cps_location=is_cps_location)

            return db_objects

        nav_hub_location_qset = filter_db_objects_by_secondary_params(nav_hub_location_qset)

        def retrieve_data_by_primary_params_and_add_to_response(db_object_qset):
            if 'id' in search_params:
                rqst_nav_hub_location_id = search_params['id']
                if rqst_nav_hub_location_id != 'all':
                    list_of_ids = search_params['id list']
                else:
                    list_of_ids = None
            else:
                rqst_nav_hub_location_id = 'all'
                list_of_ids = None

            data_list = retrieve_nav_hub_location_data_by_id(db_object_qset, rqst_nav_hub_location_id, list_of_ids,
                                                             rqst_errors)

            response_raw_data["Data"] = data_list

        retrieve_data_by_primary_params_and_add_to_response(nav_hub_location_qset)

    put_logic_function = nav_hub_location_management_put_logic
    get_logic_function = nav_hub_location_management_get_logic