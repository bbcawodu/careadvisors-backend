from django.views.generic import View
from django.utils.decorators import method_decorator
from ..utils import clean_string_value_from_dict_object
from picmodels.models import HealthcareSubsidyEligibilityByFamSize
from .tools import add_healthcare_subsidy_eligibility_data_instance_using_api_rqst_params
from .tools import modify_healthcare_subsidy_eligibility_data_instance_using_api_rqst_params
from .tools import delete_healthcare_subsidy_eligibility_data_instance_using_api_rqst_params
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
                response_raw_data = add_healthcare_subsidy_eligibility_data_instance_using_api_rqst_params(response_raw_data, post_data, post_errors)
            elif rqst_action == "Instance Modification":
                response_raw_data = modify_healthcare_subsidy_eligibility_data_instance_using_api_rqst_params(response_raw_data, post_data, post_errors)
            elif rqst_action == "Instance Deletion":
                response_raw_data = delete_healthcare_subsidy_eligibility_data_instance_using_api_rqst_params(response_raw_data, post_data, post_errors)
            else:
                post_errors.append("No valid 'Database Action' provided.")

        return response_raw_data, post_errors

    def healthcare_subsidy_eligibility_data_mgr_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        healthcare_subsidy_eligibility_data_objs = HealthcareSubsidyEligibilityByFamSize.objects.all()

        if 'id' in search_params:
            rqst_healthcare_subsidy_eligibility_data_id = search_params['id']
            if rqst_healthcare_subsidy_eligibility_data_id != 'all':
                list_of_ids = search_params['id list']
            else:
                list_of_ids = None
            response_raw_data, rqst_errors = retrieve_healthcare_subsidy_eligibility_data_by_id(response_raw_data,
                                                                                                rqst_errors,
                                                                                                healthcare_subsidy_eligibility_data_objs,
                                                                                                rqst_healthcare_subsidy_eligibility_data_id,
                                                                                                list_of_ids)
        elif 'family_size' in search_params:
            rqst_family_size = search_params['family_size']
            list_of_family_sizes = search_params['family_size_list']

            response_raw_data, rqst_errors = retrieve_healthcare_subsidy_eligibility_data_by_family_size(response_raw_data,
                                                                                                         rqst_errors,
                                                                                                         healthcare_subsidy_eligibility_data_objs,
                                                                                                         rqst_family_size,
                                                                                                         list_of_family_sizes)

        return response_raw_data, rqst_errors

    put_logic_function = healthcare_subsidy_eligibility_data_mgr_put_logic
    get_logic_function = healthcare_subsidy_eligibility_data_mgr_get_logic
