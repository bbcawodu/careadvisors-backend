from ...utils import clean_float_value_from_dict_object
from ...utils import clean_int_value_from_dict_object
from picmodels.services import add_healthcare_subsidy_eligibility_data_instance_using_validated_params
from picmodels.services import modify_healthcare_subsidy_eligibility_data_instance_using_validated_params
from picmodels.services import delete_healthcare_subsidy_eligibility_data_instance_using_validated_params


def validate_rqst_params_and_add_instance(rqst_healthcare_subsidy_eligibility_data_info, post_errors):
    add_healthcare_subsidy_eligibility_data_params = get_healthcare_subsidy_eligibility_data_mgmt_put_params(rqst_healthcare_subsidy_eligibility_data_info, post_errors)

    healthcare_subsidy_eligibility_data_obj = None
    if not post_errors:
        healthcare_subsidy_eligibility_data_obj = add_healthcare_subsidy_eligibility_data_instance_using_validated_params(add_healthcare_subsidy_eligibility_data_params, post_errors)

    return healthcare_subsidy_eligibility_data_obj


def get_healthcare_subsidy_eligibility_data_mgmt_put_params(rqst_healthcare_subsidy_eligibility_data_info, post_errors):
    family_size = clean_int_value_from_dict_object(rqst_healthcare_subsidy_eligibility_data_info, "root", "family_size", post_errors)
    if family_size and family_size < 0:
        post_errors.append("family_size must be greater than 0")

    medicaid_income_limit = clean_float_value_from_dict_object(rqst_healthcare_subsidy_eligibility_data_info, "root", "medicaid_income_limit", post_errors)
    if medicaid_income_limit and medicaid_income_limit < 0:
        post_errors.append("medicaid_income_limit must be greater than 0")

    tax_cred_for_marketplace_income_limit = clean_float_value_from_dict_object(rqst_healthcare_subsidy_eligibility_data_info, "root", "tax_cred_for_marketplace_income_limit", post_errors)
    if tax_cred_for_marketplace_income_limit and tax_cred_for_marketplace_income_limit < 0:
        post_errors.append("tax_cred_for_marketplace_income_limit must be greater than 0")

    marketplace_without_subsidies_income_level = clean_float_value_from_dict_object(rqst_healthcare_subsidy_eligibility_data_info, "root", "marketplace_without_subsidies_income_level", post_errors)
    if marketplace_without_subsidies_income_level and marketplace_without_subsidies_income_level < 0:
        post_errors.append("marketplace_without_subsidies_income_level must be greater than 0")

    return {
        "family_size": family_size,
        "medicaid_income_limit": medicaid_income_limit,
        "tax_cred_for_marketplace_income_limit": tax_cred_for_marketplace_income_limit,
        "marketplace_without_subsidies_income_level": marketplace_without_subsidies_income_level,
            }


def validate_rqst_params_and_modify_instance(rqst_healthcare_subsidy_eligibility_data_info, post_errors):
    modify_healthcare_subsidy_eligibility_data_params = get_healthcare_subsidy_eligibility_data_mgmt_put_params(rqst_healthcare_subsidy_eligibility_data_info, post_errors)
    rqst_healthcare_subsidy_eligibility_data_id = clean_int_value_from_dict_object(rqst_healthcare_subsidy_eligibility_data_info, "root", "Database ID", post_errors)

    healthcare_subsidy_eligibility_data_obj = None
    if not post_errors:
        healthcare_subsidy_eligibility_data_obj = modify_healthcare_subsidy_eligibility_data_instance_using_validated_params(modify_healthcare_subsidy_eligibility_data_params, rqst_healthcare_subsidy_eligibility_data_id, post_errors)

    return healthcare_subsidy_eligibility_data_obj


def validate_rqst_params_and_delete_instance(rqst_healthcare_subsidy_eligibility_data_info, post_errors):
    rqst_healthcare_subsidy_eligibility_data_id = clean_int_value_from_dict_object(rqst_healthcare_subsidy_eligibility_data_info, "root", "Database ID", post_errors)

    if not post_errors:
        delete_healthcare_subsidy_eligibility_data_instance_using_validated_params(rqst_healthcare_subsidy_eligibility_data_id, post_errors)
