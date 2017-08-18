import json
from picmodels.models import HealthcareSubsidyEligibilityByFamSize


def add_healthcare_subsidy_eligibility_data_instance_using_validated_params(add_healthcare_subsidy_eligibility_data_params, post_errors):
    healthcare_subsidy_eligibility_data_obj = None
    family_size = add_healthcare_subsidy_eligibility_data_params['family_size']
    found_healthcare_subsidy_eligibility_data_objs = check_for_healthcare_subsidy_eligibility_data_objs_with_given_family_size(
        family_size, post_errors)

    if not found_healthcare_subsidy_eligibility_data_objs and not post_errors:
        healthcare_subsidy_eligibility_data_obj = create_new_healthcare_subsidy_eligibility_data_obj(add_healthcare_subsidy_eligibility_data_params, post_errors)

    return healthcare_subsidy_eligibility_data_obj


def check_for_healthcare_subsidy_eligibility_data_objs_with_given_family_size(family_size, post_errors, current_healthcare_subsidy_eligibility_data_id=None):
    found_healthcare_subsidy_eligibility_data_obj = False

    healthcare_subsidy_eligibility_data_objs = HealthcareSubsidyEligibilityByFamSize.objects.filter(family_size=family_size)

    if healthcare_subsidy_eligibility_data_objs:
        found_healthcare_subsidy_eligibility_data_obj = True

        healthcare_subsidy_eligibility_data_ids = []
        len_of_eligibility_data_qset = len(healthcare_subsidy_eligibility_data_objs)
        for healthcare_subsidy_eligibility_data_obj in healthcare_subsidy_eligibility_data_objs:
            healthcare_subsidy_eligibility_data_ids.append(healthcare_subsidy_eligibility_data_obj.id)

        if len_of_eligibility_data_qset > 1:
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

    if not post_errors:
        healthcare_subsidy_eligibility_data_obj.save()

    return healthcare_subsidy_eligibility_data_obj


def modify_healthcare_subsidy_eligibility_data_instance_using_validated_params(modify_healthcare_subsidy_eligibility_data_params, rqst_healthcare_subsidy_eligibility_data_id, post_errors):
    healthcare_subsidy_eligibility_data_obj = None
    family_size = modify_healthcare_subsidy_eligibility_data_params['family_size']
    found_healthcare_subsidy_eligibility_data_objs = check_for_healthcare_subsidy_eligibility_data_objs_with_given_family_size(
        family_size, post_errors, rqst_healthcare_subsidy_eligibility_data_id)

    if not found_healthcare_subsidy_eligibility_data_objs and not post_errors:
        healthcare_subsidy_eligibility_data_obj = modify_healthcare_subsidy_eligibility_data_obj(modify_healthcare_subsidy_eligibility_data_params, rqst_healthcare_subsidy_eligibility_data_id, post_errors)

    return healthcare_subsidy_eligibility_data_obj


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

    if not post_errors:
        healthcare_subsidy_eligibility_data_obj.save()

    return healthcare_subsidy_eligibility_data_obj


def delete_healthcare_subsidy_eligibility_data_instance_using_validated_params(rqst_healthcare_subsidy_eligibility_data_id, post_errors):
    try:
        healthcare_subsidy_eligibility_data_obj = HealthcareSubsidyEligibilityByFamSize.objects.get(id=rqst_healthcare_subsidy_eligibility_data_id)
        healthcare_subsidy_eligibility_data_obj.delete()
    except HealthcareSubsidyEligibilityByFamSize.DoesNotExist:
        post_errors.append("Healthcare subsidy eligibility data instance does not exist for database id: {}".format(rqst_healthcare_subsidy_eligibility_data_id))
