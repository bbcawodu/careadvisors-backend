import json
from picmodels.models import HealthcareSubsidyEligibilityByFamSize
from ...utils import clean_float_value_from_dict_object
from ...utils import clean_int_value_from_dict_object


def add_healthcare_subsidy_eligibility_data_instance_using_api_rqst_params(response_raw_data, rqst_healthcare_subsidy_eligibility_data_info, post_errors):
    add_healthcare_subsidy_eligibility_data_params = get_healthcare_subsidy_eligibility_data_mgmt_put_params(rqst_healthcare_subsidy_eligibility_data_info, post_errors)

    if len(post_errors) == 0:
        family_size = add_healthcare_subsidy_eligibility_data_params['family_size']

        found_healthcare_subsidy_eligibility_data_objs = check_for_healthcare_subsidy_eligibility_data_objs_with_given_family_size(
            family_size, post_errors)

        if not found_healthcare_subsidy_eligibility_data_objs and len(post_errors) == 0:
            healthcare_subsidy_eligibility_data_obj = create_new_healthcare_subsidy_eligibility_data_obj(add_healthcare_subsidy_eligibility_data_params, post_errors)

            if len(post_errors) == 0:
                response_raw_data['Data']["Database ID"] = healthcare_subsidy_eligibility_data_obj.id

    return response_raw_data


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


def check_for_healthcare_subsidy_eligibility_data_objs_with_given_family_size(family_size, post_errors, current_healthcare_subsidy_eligibility_data_id=None):
    found_healthcare_subsidy_eligibility_data_obj = False

    healthcare_subsidy_eligibility_data_objs = HealthcareSubsidyEligibilityByFamSize.objects.filter(family_size=family_size)

    if healthcare_subsidy_eligibility_data_objs:
        found_healthcare_subsidy_eligibility_data_obj = True

        healthcare_subsidy_eligibility_data_ids = []
        for healthcare_subsidy_eligibility_data_obj in healthcare_subsidy_eligibility_data_objs:
            healthcare_subsidy_eligibility_data_ids.append(healthcare_subsidy_eligibility_data_obj.id)

        if healthcare_subsidy_eligibility_data_objs.count() > 1:
            post_errors.append(
                "Multiple instances of healthcare subsidy eligibility data with family size: {} already exist in db. (Hint - Delete one and modify the remaining) id's: {}".format(
                    family_size, json.dumps(healthcare_subsidy_eligibility_data_ids)))
        else:
            if not current_healthcare_subsidy_eligibility_data_id or current_healthcare_subsidy_eligibility_data_id not in healthcare_subsidy_eligibility_data_ids:
                post_errors.append(
                    "Healthcare subsidy eligibility data with family size: {} already exists in db. (Hint - Modify that entry) id: {}".format(
                        family_size, healthcare_subsidy_eligibility_data_ids[0]))
            else:
                found_healthcare_subsidy_eligibility_data_obj = False

    return found_healthcare_subsidy_eligibility_data_obj


def create_new_healthcare_subsidy_eligibility_data_obj(healthcare_subsidy_eligibility_data_params, post_errors):
    healthcare_subsidy_eligibility_data_obj = HealthcareSubsidyEligibilityByFamSize()
    healthcare_subsidy_eligibility_data_obj.family_size = healthcare_subsidy_eligibility_data_params['family_size']
    healthcare_subsidy_eligibility_data_obj.medicaid_income_limit = healthcare_subsidy_eligibility_data_params['medicaid_income_limit']
    healthcare_subsidy_eligibility_data_obj.tax_cred_for_marketplace_income_limit = healthcare_subsidy_eligibility_data_params['tax_cred_for_marketplace_income_limit']
    healthcare_subsidy_eligibility_data_obj.marketplace_without_subsidies_income_level = healthcare_subsidy_eligibility_data_params['marketplace_without_subsidies_income_level']

    if len(post_errors) == 0:
        healthcare_subsidy_eligibility_data_obj.save()

    return healthcare_subsidy_eligibility_data_obj


def modify_healthcare_subsidy_eligibility_data_instance_using_api_rqst_params(response_raw_data, rqst_healthcare_subsidy_eligibility_data_info, post_errors):
    modify_healthcare_subsidy_eligibility_data_params = get_healthcare_subsidy_eligibility_data_mgmt_put_params(rqst_healthcare_subsidy_eligibility_data_info, post_errors)
    rqst_healthcare_subsidy_eligibility_data_id = clean_int_value_from_dict_object(rqst_healthcare_subsidy_eligibility_data_info, "root", "Database ID", post_errors)

    if len(post_errors) == 0:
        family_size = modify_healthcare_subsidy_eligibility_data_params['family_size']
        found_healthcare_subsidy_eligibility_data_objs = check_for_healthcare_subsidy_eligibility_data_objs_with_given_family_size(
            family_size, post_errors, rqst_healthcare_subsidy_eligibility_data_id)

        if not found_healthcare_subsidy_eligibility_data_objs and len(post_errors) == 0:
            healthcare_subsidy_eligibility_data_obj = modify_healthcare_subsidy_eligibility_data_obj(modify_healthcare_subsidy_eligibility_data_params, rqst_healthcare_subsidy_eligibility_data_id, post_errors)

            if len(post_errors) == 0:
                response_raw_data['Data']["Database ID"] = healthcare_subsidy_eligibility_data_obj.id

    return response_raw_data


def modify_healthcare_subsidy_eligibility_data_obj(healthcare_subsidy_eligibility_data_params, healthcare_subsidy_eligibility_data_id, post_errors):
    healthcare_subsidy_eligibility_data_obj = None
    try:
        healthcare_subsidy_eligibility_data_obj = HealthcareSubsidyEligibilityByFamSize.objects.get(id=healthcare_subsidy_eligibility_data_id)
        healthcare_subsidy_eligibility_data_obj.family_size = healthcare_subsidy_eligibility_data_params['family_size']
        healthcare_subsidy_eligibility_data_obj.medicaid_income_limit = healthcare_subsidy_eligibility_data_params['medicaid_income_limit']
        healthcare_subsidy_eligibility_data_obj.tax_cred_for_marketplace_income_limit = healthcare_subsidy_eligibility_data_params['tax_cred_for_marketplace_income_limit']
        healthcare_subsidy_eligibility_data_obj.marketplace_without_subsidies_income_level = healthcare_subsidy_eligibility_data_params['marketplace_without_subsidies_income_level']
    except HealthcareSubsidyEligibilityByFamSize.DoesNotExist:
        post_errors.append("Healthcare subsidy eligibility data instance does not exist for database id: {}".format(healthcare_subsidy_eligibility_data_id))

    if len(post_errors) == 0:
        healthcare_subsidy_eligibility_data_obj.save()

    return healthcare_subsidy_eligibility_data_obj


def delete_healthcare_subsidy_eligibility_data_instance_using_api_rqst_params(response_raw_data, rqst_healthcare_subsidy_eligibility_data_info, post_errors):
    rqst_healthcare_subsidy_eligibility_data_id = clean_int_value_from_dict_object(rqst_healthcare_subsidy_eligibility_data_info, "root", "Database ID", post_errors)

    if len(post_errors) == 0:
        try:
            healthcare_subsidy_eligibility_data_obj = HealthcareSubsidyEligibilityByFamSize.objects.get(id=rqst_healthcare_subsidy_eligibility_data_id)
            healthcare_subsidy_eligibility_data_obj.delete()
            response_raw_data['Data']["Database ID"] = "Deleted"
        except HealthcareSubsidyEligibilityByFamSize.DoesNotExist:
            post_errors.append("Healthcare subsidy eligibility data instance does not exist for database id: {}".format(rqst_healthcare_subsidy_eligibility_data_id))

    return response_raw_data
