from django.views.generic import View

from picbackend.views.utils import JSONGETRspMixin
from picbackend.views.utils import JSONPUTRspMixin

from picmodels.models import HealthcareSubsidyEligibilityByFamSize

from .tools import validate_put_rqst_params


# Need to abstract common variables in get and post class methods into class attributes
class HealthcareSubsidyEligibilityDataMgrView(JSONPUTRspMixin, JSONGETRspMixin, View):
    def healthcare_subsidy_eligibility_data_mgr_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        validated_put_rqst_params = validate_put_rqst_params(rqst_body, rqst_errors)
        rqst_action = validated_put_rqst_params['rqst_action']

        if not rqst_errors:
            if rqst_action == "create":
                subsidy_eligibility_data_obj = HealthcareSubsidyEligibilityByFamSize.create_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )

                if subsidy_eligibility_data_obj:
                    response_raw_data['Data']["row"] = subsidy_eligibility_data_obj.return_values_dict()
            elif rqst_action == "update":
                subsidy_eligibility_data_obj = HealthcareSubsidyEligibilityByFamSize.update_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )

                if subsidy_eligibility_data_obj:
                    response_raw_data['Data']["row"] = subsidy_eligibility_data_obj.return_values_dict()
            elif rqst_action == "delete":
                HealthcareSubsidyEligibilityByFamSize.delete_row_w_validated_params(
                    validated_put_rqst_params,
                    rqst_errors
                )

                if not rqst_errors:
                    response_raw_data['Data']["row"] = "Deleted"
            else:
                rqst_errors.append("No valid 'db_action' provided.")

    def healthcare_subsidy_eligibility_data_mgr_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        def retrieve_data_by_primary_params_and_add_to_response():
            data_list = []

            if 'id' in validated_GET_rqst_params:
                rqst_healthcare_subsidy_eligibility_data_id = validated_GET_rqst_params['id']
                if rqst_healthcare_subsidy_eligibility_data_id != 'all':
                    list_of_ids = validated_GET_rqst_params['id_list']
                else:
                    list_of_ids = []

                data_list = HealthcareSubsidyEligibilityByFamSize.retrieve_healthcare_subsidy_eligibility_data_by_id(
                    rqst_healthcare_subsidy_eligibility_data_id,
                    list_of_ids,
                    rqst_errors
                )

            elif 'family_size' in validated_GET_rqst_params:
                list_of_family_sizes = validated_GET_rqst_params['family_size_list']

                data_list = HealthcareSubsidyEligibilityByFamSize.retrieve_healthcare_subsidy_eligibility_data_by_family_size(
                    list_of_family_sizes,
                    rqst_errors
                )
            else:
                rqst_errors.append('No Valid Parameters')

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response()

    parse_PUT_request_and_add_response = healthcare_subsidy_eligibility_data_mgr_put_logic

    accepted_GET_request_parameters = [
        "id",
        "family_size"
    ]
    parse_GET_request_and_add_response = healthcare_subsidy_eligibility_data_mgr_get_logic
