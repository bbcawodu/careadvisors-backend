"""
This module defines views that handle hospital/provider locations for provider networks contracted with PIC
"""

from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ...utils import clean_string_value_from_dict_object
from picmodels.models import ConsumerSpecificConcern
from .tools import validate_rqst_params_and_add_instance
from .tools import validate_rqst_params_and_modify_instance
from .tools import validate_rqst_params_and_add_general_concern_to_instance
from .tools import validate_rqst_params_and_remove_general_concern_from_instance
from .tools import validate_rqst_params_and_delete_instance
from .tools import retrieve_specific_concern_data_by_id
from .tools import retrieve_specific_concern_data_by_question
from .tools import retrieve_specific_concern_data_by_gen_concern_name
from .tools import retrieve_specific_concern_data_by_gen_concern_id_subset
from .tools import retrieve_specific_concern_data_by_gen_concern_id
from ...utils import JSONPUTRspMixin
from ...utils import JSONGETRspMixin


#Need to abstract common variables in get and post class methods into class attributes
class SpecificConcernsManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles healthcare carrier related requests
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SpecificConcernsManagementView, self).dispatch(request, *args, **kwargs)

    def specific_concerns_management_put_logic(self, post_data, response_raw_data, post_errors):
        # Retrieve database action from post data
        rqst_action = clean_string_value_from_dict_object(post_data, "root", "Database Action", post_errors)

        # If there are no parsing errors, process PUT data based on database action
        if not post_errors:
            specific_concern_obj = None

            if rqst_action == "Add Specific Concern":
                specific_concern_obj = validate_rqst_params_and_add_instance(post_data, post_errors)
            elif rqst_action == "Modify Specific Concern":
                specific_concern_obj = validate_rqst_params_and_modify_instance(post_data, post_errors)
            elif rqst_action == "Modify Specific Concern - add_general_concern":
                specific_concern_obj = validate_rqst_params_and_add_general_concern_to_instance(post_data, post_errors)
            elif rqst_action == "Modify Specific Concern - remove_general_concern":
                specific_concern_obj = validate_rqst_params_and_remove_general_concern_from_instance(post_data, post_errors)
            elif rqst_action == "Delete Specific Concern":
                validate_rqst_params_and_delete_instance(post_data, post_errors)

                if not post_errors:
                    response_raw_data['Data']["Database ID"] = "Deleted"
            else:
                post_errors.append("No valid 'Database Action' provided.")

            if specific_concern_obj:
                response_raw_data['Data']["Database ID"] = specific_concern_obj.id

    def specific_concerns_management_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        specific_concerns = ConsumerSpecificConcern.objects.all()

        def retrieve_data_by_primary_params_and_add_to_response(db_objects):
            data_list = []

            if 'id' in search_params:
                rqst_specific_concern_id = search_params['id']
                if rqst_specific_concern_id != 'all':
                    list_of_ids = search_params['id list']
                else:
                    list_of_ids = None

                data_list = retrieve_specific_concern_data_by_id(db_objects, rqst_specific_concern_id, list_of_ids, rqst_errors)
            elif 'question' in search_params:
                rqst_question = search_params['question']

                data_list = retrieve_specific_concern_data_by_question(db_objects, rqst_question, rqst_errors)
            elif 'gen_concern_name' in search_params:
                rqst_gen_concern_name = search_params['gen_concern_name']

                data_list = retrieve_specific_concern_data_by_gen_concern_name(db_objects, rqst_gen_concern_name, rqst_errors)
            elif 'gen_concern_id_subset' in search_params:
                list_of_gen_concern_ids = search_params['gen_concern_id_subset_list']

                data_list = retrieve_specific_concern_data_by_gen_concern_id_subset(db_objects, list_of_gen_concern_ids, rqst_errors)
            elif 'gen_concern_id' in search_params:
                list_of_gen_concern_ids = search_params['gen_concern_id_list']

                data_list = retrieve_specific_concern_data_by_gen_concern_id(list_of_gen_concern_ids, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response(specific_concerns)

    put_logic_function = specific_concerns_management_put_logic

    accepted_get_parameters = [
        "id",
        "question",
        "gen_concern_name",
        "gen_concern_id_subset",
        "gen_concern_id"
    ]
    get_logic_function = specific_concerns_management_get_logic
