from django.views.generic import View

from picbackend.views.utils import JSONGETRspMixin
from picbackend.views.utils import JSONPUTRspMixin
from picbackend.views.utils import clean_string_value_from_dict_object
from picmodels.models import HealthcareSubsidyEligibilityByFamSize
from .tools import retrieve_healthcare_subsidy_eligibility_data_by_family_size
from .tools import retrieve_healthcare_subsidy_eligibility_data_by_id
from .tools import validate_rqst_params_and_add_instance
from .tools import validate_rqst_params_and_delete_instance
from .tools import validate_rqst_params_and_modify_instance


# Need to abstract common variables in get and post class methods into class attributes
class HealthcareSubsidyEligibilityDataMgrView(JSONPUTRspMixin, JSONGETRspMixin, View):
    def healthcare_subsidy_eligibility_data_mgr_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        # Retrieve database action from post data
        rqst_action = clean_string_value_from_dict_object(rqst_body, "root", "Database Action", rqst_errors)

        # If there are no parsing errors, process PUT data based on database action
        if not rqst_errors:
            if rqst_action == "Instance Addition":
                subsidy_eligibility_data_obj = validate_rqst_params_and_add_instance(rqst_body, rqst_errors)

                if not rqst_errors:
                    response_raw_data['Data']["Database ID"] = subsidy_eligibility_data_obj.id
            elif rqst_action == "Instance Modification":
                subsidy_eligibility_data_obj = validate_rqst_params_and_modify_instance(rqst_body, rqst_errors)

                if not rqst_errors:
                    response_raw_data['Data']["Database ID"] = subsidy_eligibility_data_obj.id
            elif rqst_action == "Instance Deletion":
                validate_rqst_params_and_delete_instance(rqst_body, rqst_errors)

                if not rqst_errors:
                    response_raw_data['Data']["Database ID"] = "Deleted"
            else:
                rqst_errors.append("No valid 'Database Action' provided.")

    def healthcare_subsidy_eligibility_data_mgr_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        healthcare_subsidy_eligibility_data_objs = HealthcareSubsidyEligibilityByFamSize.objects.all()

        def retrieve_data_by_primary_params_and_add_to_response(db_objs):
            data_list = []

            if 'id' in validated_GET_rqst_params:
                rqst_healthcare_subsidy_eligibility_data_id = validated_GET_rqst_params['id']
                if rqst_healthcare_subsidy_eligibility_data_id != 'all':
                    list_of_ids = validated_GET_rqst_params['id_list']
                else:
                    list_of_ids = []
                data_list = retrieve_healthcare_subsidy_eligibility_data_by_id(db_objs,
                                                                               rqst_healthcare_subsidy_eligibility_data_id,
                                                                               list_of_ids, rqst_errors)
            elif 'family_size' in validated_GET_rqst_params:
                list_of_family_sizes = validated_GET_rqst_params['family_size_list']

                data_list = retrieve_healthcare_subsidy_eligibility_data_by_family_size(db_objs,
                                                                                        list_of_family_sizes, rqst_errors)
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response(healthcare_subsidy_eligibility_data_objs)

    parse_PUT_request_and_add_response = healthcare_subsidy_eligibility_data_mgr_put_logic

    accepted_GET_request_parameters = [
        "id",
        "family_size"
    ]
    parse_GET_request_and_add_response = healthcare_subsidy_eligibility_data_mgr_get_logic
