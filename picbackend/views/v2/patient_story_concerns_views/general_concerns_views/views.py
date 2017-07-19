"""
This module defines views that handle general concerns requests for the Navigator Online Plus patient story conversation
flow
"""

from django.views.generic import View
from django.utils.decorators import method_decorator
from ...utils import clean_string_value_from_dict_object
from picmodels.models import ConsumerGeneralConcern
from .tools import validate_rqst_params_and_add_instance
from .tools import validate_rqst_params_and_modify_instance
from .tools import validate_rqst_params_and_delete_instance
from .tools import retrieve_general_concerns_by_id
from .tools import retrieve_general_concerns_by_name
from django.views.decorators.csrf import csrf_exempt
from ...utils import JSONPUTRspMixin
from ...utils import JSONGETRspMixin


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
                general_concern_obj = validate_rqst_params_and_add_instance(post_data, post_errors)

                if general_concern_obj:
                    response_raw_data['Data']["Database ID"] = general_concern_obj.id
            elif rqst_action == "Concern Modification":
                general_concern_obj = validate_rqst_params_and_modify_instance(post_data, post_errors)

                if general_concern_obj:
                    response_raw_data['Data']["Database ID"] = general_concern_obj.id
            elif rqst_action == "Concern Deletion":
                validate_rqst_params_and_delete_instance(post_data, post_errors)

                if not post_errors:
                    response_raw_data['Data']["Database ID"] = "Deleted"
            else:
                post_errors.append("No valid 'Database Action' provided.")

    def general_concerns_management_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        general_concerns = ConsumerGeneralConcern.objects.all()

        def retrieve_data_by_primary_params_and_add_to_response(db_objects):
            data_list = []

            if 'id' in search_params:
                rqst_general_concerns_id = search_params['id']
                if rqst_general_concerns_id != 'all':
                    list_of_ids = search_params['id_list']
                else:
                    list_of_ids = None

                data_list = retrieve_general_concerns_by_id(db_objects, rqst_general_concerns_id, list_of_ids, rqst_errors)
            elif 'name' in search_params:
                rqst_name = search_params['name']

                data_list = retrieve_general_concerns_by_name(db_objects, rqst_name, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response(general_concerns)

    put_logic_function = general_concerns_management_put_logic

    accepted_get_parameters = [
        "id",
        "name"
    ]
    get_logic_function = general_concerns_management_get_logic
