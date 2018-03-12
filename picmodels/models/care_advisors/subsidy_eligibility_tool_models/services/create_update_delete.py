import json


def create_row_w_validated_params(cls, validated_params, rqst_errors):
    new_row = None
    family_size = validated_params['family_size']

    found_healthcare_subsidy_eligibility_data_objs = cls.check_for_rows_w_given_family_size(family_size, rqst_errors)

    if not found_healthcare_subsidy_eligibility_data_objs and not rqst_errors:
        new_row = cls()
        new_row.family_size = family_size
        new_row.medicaid_income_limit = validated_params['medicaid_income_limit']
        new_row.tax_cred_for_marketplace_income_limit = validated_params['tax_cred_for_marketplace_income_limit']
        new_row.marketplace_without_subsidies_income_level = validated_params['marketplace_without_subsidies_income_level']

        new_row.save()

    return new_row


def update_row_w_validated_params(cls, validated_params, rqst_errors):
    row_to_modify = None
    family_size = validated_params['family_size']
    rqst_id = validated_params['rqst_id']

    found_healthcare_subsidy_eligibility_data_objs = cls.check_for_rows_w_given_family_size(family_size, rqst_errors, rqst_id)

    if not found_healthcare_subsidy_eligibility_data_objs and not rqst_errors:
        try:
            row_to_modify = cls.objects.get(id=rqst_id)

            if "family_size" in validated_params:
                row_to_modify.family_size = validated_params['family_size']

            if "medicaid_income_limit" in validated_params:
                row_to_modify.medicaid_income_limit = validated_params['medicaid_income_limit']

            if 'tax_cred_for_marketplace_income_limit' in validated_params:
                row_to_modify.tax_cred_for_marketplace_income_limit = validated_params['tax_cred_for_marketplace_income_limit']

            if 'marketplace_without_subsidies_income_level' in validated_params:
                row_to_modify.marketplace_without_subsidies_income_level = validated_params['marketplace_without_subsidies_income_level']
        except cls.DoesNotExist:
            rqst_errors.append(
                "Healthcare subsidy eligibility data instance does not exist for database id: {}".format(rqst_id))

        if not rqst_errors:
            row_to_modify.save()

    return row_to_modify


def delete_row_w_validated_params(cls, validated_params, post_errors):
    rqst_id = validated_params['rqst_id']

    try:
        healthcare_subsidy_eligibility_data_obj = cls.objects.get(id=rqst_id)
        healthcare_subsidy_eligibility_data_obj.delete()
    except cls.DoesNotExist:
        post_errors.append("Healthcare subsidy eligibility data instance does not exist for database id: {}".format(rqst_id))


def check_for_rows_w_given_family_size(cls, family_size, rqst_errors, current_row_id=None):
    found_healthcare_subsidy_eligibility_data_obj = False

    healthcare_subsidy_eligibility_data_objs = cls.objects.filter(family_size=family_size)

    if healthcare_subsidy_eligibility_data_objs:
        found_healthcare_subsidy_eligibility_data_obj = True

        healthcare_subsidy_eligibility_data_ids = []
        len_of_eligibility_data_qset = len(healthcare_subsidy_eligibility_data_objs)
        for healthcare_subsidy_eligibility_data_obj in healthcare_subsidy_eligibility_data_objs:
            healthcare_subsidy_eligibility_data_ids.append(healthcare_subsidy_eligibility_data_obj.id)

        if len_of_eligibility_data_qset > 1:
            rqst_errors.append(
                "Multiple instances of healthcare subsidy eligibility data with family size: {} already exist in db. (Hint - Delete one and modify the remaining) id's: {}".format(
                    family_size, json.dumps(healthcare_subsidy_eligibility_data_ids)))
        else:
            if not current_row_id or current_row_id not in healthcare_subsidy_eligibility_data_ids:
                rqst_errors.append(
                    "Healthcare subsidy eligibility data with family size: {} already exists in db. (Hint - Modify that entry) id: {}".format(
                        family_size, healthcare_subsidy_eligibility_data_ids[0]))
            else:
                found_healthcare_subsidy_eligibility_data_obj = False

    return found_healthcare_subsidy_eligibility_data_obj
