from picbackend.views.utils import clean_float_value_from_dict_object
from picbackend.views.utils import clean_int_value_from_dict_object
from picbackend.views.utils import clean_string_value_from_dict_object


def validate_put_rqst_params(rqst_body, rqst_errors):
    validated_params = {
        'rqst_action': clean_string_value_from_dict_object(rqst_body, "root", "db_action", rqst_errors)
    }

    rqst_action = validated_params['rqst_action']

    if rqst_action == 'create':
        validate_create_row_params(rqst_body, validated_params, rqst_errors)
    elif rqst_action == 'update':
        validated_params['rqst_id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)
        validate_update_row_params(rqst_body, validated_params, rqst_errors)
    elif rqst_action == 'delete':
        validated_params['rqst_id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)

    return validated_params


def validate_create_row_params(rqst_body, validated_params, rqst_errors):
    family_size = clean_int_value_from_dict_object(rqst_body, "root", "family_size", rqst_errors)
    if family_size:
        if family_size < 0:
            rqst_errors.append("family_size must be greater than 0")

    medicaid_income_limit = clean_float_value_from_dict_object(rqst_body, "root", "medicaid_income_limit", rqst_errors)
    if medicaid_income_limit:
        if medicaid_income_limit < 0:
            rqst_errors.append("medicaid_income_limit must be greater than 0")

    tax_cred_for_marketplace_income_limit = clean_float_value_from_dict_object(rqst_body, "root", "tax_cred_for_marketplace_income_limit", rqst_errors)
    if tax_cred_for_marketplace_income_limit:
        if tax_cred_for_marketplace_income_limit < 0:
            rqst_errors.append("tax_cred_for_marketplace_income_limit must be greater than 0")

    marketplace_without_subsidies_income_level = clean_float_value_from_dict_object(rqst_body, "root", "marketplace_without_subsidies_income_level", rqst_errors)
    if marketplace_without_subsidies_income_level:
        if marketplace_without_subsidies_income_level < 0:
            rqst_errors.append("marketplace_without_subsidies_income_level must be greater than 0")

    validated_params["family_size"] = family_size
    validated_params["medicaid_income_limit"] = medicaid_income_limit
    validated_params["tax_cred_for_marketplace_income_limit"] = tax_cred_for_marketplace_income_limit
    validated_params["marketplace_without_subsidies_income_level"] = marketplace_without_subsidies_income_level


def validate_update_row_params(rqst_body, validated_params, rqst_errors):
    if "family_size" in rqst_body:
        family_size = clean_int_value_from_dict_object(rqst_body, "root", "family_size", rqst_errors)
        if family_size:
            if family_size < 0:
                rqst_errors.append("family_size must be greater than 0")
        validated_params["family_size"] = family_size

    if "medicaid_income_limit" in rqst_body:
        medicaid_income_limit = clean_float_value_from_dict_object(
            rqst_body,
            "root",
            "medicaid_income_limit",
            rqst_errors
        )
        if medicaid_income_limit:
            if medicaid_income_limit < 0:
                rqst_errors.append("medicaid_income_limit must be greater than 0")
        validated_params["medicaid_income_limit"] = medicaid_income_limit

    if "tax_cred_for_marketplace_income_limit" in rqst_body:
        tax_cred_for_marketplace_income_limit = clean_float_value_from_dict_object(
            rqst_body,
            "root",
            "tax_cred_for_marketplace_income_limit",
            rqst_errors
        )
        if tax_cred_for_marketplace_income_limit:
            if tax_cred_for_marketplace_income_limit < 0:
                rqst_errors.append("tax_cred_for_marketplace_income_limit must be greater than 0")
        validated_params["tax_cred_for_marketplace_income_limit"] = tax_cred_for_marketplace_income_limit

    if "marketplace_without_subsidies_income_level" in rqst_body:
        marketplace_without_subsidies_income_level = clean_float_value_from_dict_object(
            rqst_body,
            "root",
            "marketplace_without_subsidies_income_level",
            rqst_errors
        )
        if marketplace_without_subsidies_income_level:
            if marketplace_without_subsidies_income_level < 0:
                rqst_errors.append("marketplace_without_subsidies_income_level must be greater than 0")
        validated_params["marketplace_without_subsidies_income_level"] = marketplace_without_subsidies_income_level
