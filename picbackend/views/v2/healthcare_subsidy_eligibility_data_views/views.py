from django.views.generic import View
from django.utils.decorators import method_decorator
from ..utils import clean_string_value_from_dict_object
from picmodels.models import HealthcareSubsidyEligibilityByFamSize
from .tools import validate_rqst_params_and_add_instance
from .tools import validate_rqst_params_and_modify_instance
from .tools import validate_rqst_params_and_delete_instance
from .tools import retrieve_healthcare_subsidy_eligibility_data_by_id
from .tools import retrieve_healthcare_subsidy_eligibility_data_by_family_size
from django.views.decorators.csrf import csrf_exempt
from ..base import JSONPUTRspMixin
from ..base import JSONGETRspMixin


#Need to abstract common variables in get and post class methods into class attributes
class HealthcareSubsidyEligibilityDataMgrView(JSONPUTRspMixin, JSONGETRspMixin, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(HealthcareSubsidyEligibilityDataMgrView, self).dispatch(request, *args, **kwargs)

    def healthcare_subsidy_eligibility_data_mgr_put_logic(self, post_data, response_raw_data, post_errors):
        # Retrieve database action from post data
        rqst_action = clean_string_value_from_dict_object(post_data, "root", "Database Action", post_errors)

        # If there are no parsing errors, process PUT data based on database action
        if not post_errors:
            if rqst_action == "Instance Addition":
                subsidy_eligibility_data_obj = validate_rqst_params_and_add_instance(post_data, post_errors)

                if not post_errors:
                    response_raw_data['Data']["Database ID"] = subsidy_eligibility_data_obj.id
            elif rqst_action == "Instance Modification":
                subsidy_eligibility_data_obj = validate_rqst_params_and_modify_instance(post_data, post_errors)

                if not post_errors:
                    response_raw_data['Data']["Database ID"] = subsidy_eligibility_data_obj.id
            elif rqst_action == "Instance Deletion":
                validate_rqst_params_and_delete_instance(post_data, post_errors)

                if not post_errors:
                    response_raw_data['Data']["Database ID"] = "Deleted"
            else:
                post_errors.append("No valid 'Database Action' provided.")

    def healthcare_subsidy_eligibility_data_mgr_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        healthcare_subsidy_eligibility_data_objs = HealthcareSubsidyEligibilityByFamSize.objects.all()

        def retrieve_data_by_primary_params_and_add_to_response(db_objs):
            data_list = []

            if 'id' in search_params:
                rqst_healthcare_subsidy_eligibility_data_id = search_params['id']
                if rqst_healthcare_subsidy_eligibility_data_id != 'all':
                    list_of_ids = search_params['id list']
                else:
                    list_of_ids = []
                data_list = retrieve_healthcare_subsidy_eligibility_data_by_id(db_objs,
                                                                               rqst_healthcare_subsidy_eligibility_data_id,
                                                                               list_of_ids, rqst_errors)
            elif 'family_size' in search_params:
                list_of_family_sizes = search_params['family_size_list']

                data_list = retrieve_healthcare_subsidy_eligibility_data_by_family_size(db_objs,
                                                                                        list_of_family_sizes, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response(healthcare_subsidy_eligibility_data_objs)

    put_logic_function = healthcare_subsidy_eligibility_data_mgr_put_logic
    get_logic_function = healthcare_subsidy_eligibility_data_mgr_get_logic
