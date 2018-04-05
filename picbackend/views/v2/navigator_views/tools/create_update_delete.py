from django import forms
from django.core.validators import validate_email
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from picbackend.views.utils import clean_int_value_from_dict_object
from picbackend.views.utils import clean_list_value_from_dict_object
from picbackend.views.utils import clean_string_value_from_dict_object
from picbackend.views.utils import clean_dict_value_from_dict_object


def validate_put_rqst_params(rqst_body, rqst_errors):
    validated_params = {
        'rqst_action': clean_string_value_from_dict_object(rqst_body, "root", "db_action", rqst_errors)
    }

    rqst_action = validated_params['rqst_action']

    if rqst_action == 'create':
        validate_create_row_params(rqst_body, validated_params, rqst_errors)
    elif rqst_action == 'update':
        validated_params['id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)
        validate_update_row_params(rqst_body, validated_params, rqst_errors)
    elif rqst_action == 'delete':
        validated_params['id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)

    return validated_params


def validate_create_row_params(rqst_body, validated_params, rqst_errors):
    email = clean_string_value_from_dict_object(rqst_body, "root", "email", rqst_errors)
    if email and not rqst_errors:
        try:
            validate_email(email)
        except forms.ValidationError:
            rqst_errors.append("{!s} must be a valid email address".format(email))
    validated_params["email"] = email

    mpn = clean_string_value_from_dict_object(
        rqst_body,
        "root",
        "mpn",
        rqst_errors,
        empty_string_allowed=True,
        none_allowed=True
    )
    if mpn is None:
        mpn = ''
    validated_params["mpn"] = mpn

    first_name = clean_string_value_from_dict_object(rqst_body, "root", "first_name", rqst_errors)
    validated_params["first_name"] = first_name

    last_name = clean_string_value_from_dict_object(rqst_body, "root", "last_name", rqst_errors)
    validated_params["last_name"] = last_name

    county = clean_string_value_from_dict_object(rqst_body, "root", "county", rqst_errors)
    validated_params["county"] = county

    type = clean_string_value_from_dict_object(rqst_body, "root", "type", rqst_errors)
    validated_params["type"] = type

    if 'add_base_locations' in rqst_body:
        add_base_location_names = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "add_base_locations",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_base_location_names = []
        for base_location_name in add_base_location_names:
            if not isinstance(base_location_name, str):
                rqst_errors.append('Error: A base_location_name in \'add_base_locations\' is not a string.')
                continue

            validated_base_location_names.append(base_location_name)

        validated_params['add_base_locations'] = validated_base_location_names

    validate_nav_signup_params(rqst_body, validated_params, rqst_errors)


def validate_update_row_params(rqst_body, validated_params, rqst_errors):
    if "email" in rqst_body:
        email = clean_string_value_from_dict_object(rqst_body, "root", "email", rqst_errors)
        if email and not rqst_errors:
            try:
                validate_email(email)
            except forms.ValidationError:
                rqst_errors.append("{!s} must be a valid email address".format(email))
        validated_params["email"] = email

    if "mpn" in rqst_body:
        mpn = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "mpn",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )
        if mpn is None:
            mpn = ''
        validated_params["mpn"] = mpn

    if "first_name" in rqst_body:
        first_name = clean_string_value_from_dict_object(rqst_body, "root", "first_name", rqst_errors)
        validated_params["first_name"] = first_name

    if "last_name" in rqst_body:
        last_name = clean_string_value_from_dict_object(rqst_body, "root", "last_name", rqst_errors)
        validated_params["last_name"] = last_name

    if "county" in rqst_body:
        county = clean_string_value_from_dict_object(rqst_body, "root", "county", rqst_errors)
        validated_params["county"] = county

    if "type" in rqst_body:
        type = clean_string_value_from_dict_object(rqst_body, "root", "type", rqst_errors)
        validated_params["type"] = type

    if 'add_base_locations' in rqst_body:
        add_base_location_names = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "add_base_locations",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_base_location_names = []
        for base_location_name in add_base_location_names:
            if not isinstance(base_location_name, str):
                rqst_errors.append('Error: A base_location_name in \'add_base_locations\' is not a string.')
                continue

            validated_base_location_names.append(base_location_name)

        validated_params['add_base_locations'] = validated_base_location_names
    elif 'remove_base_locations' in rqst_body:
        remove_base_location_names = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "remove_base_locations",
            rqst_errors
        )

        validated_base_location_names = []
        for base_location_name in remove_base_location_names:
            if not isinstance(base_location_name, str):
                rqst_errors.append('Error: A base_location_name in \'remove_base_locations\' is not a string.')
                continue

            validated_base_location_names.append(base_location_name)

        validated_params['remove_base_locations'] = validated_base_location_names

    validate_nav_signup_params(rqst_body, validated_params, rqst_errors)


def validate_nav_signup_params(rqst_body, validated_params, rqst_errors):
    if 'add_healthcare_locations_worked' in rqst_body:
        add_healthcare_locations_worked = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "add_healthcare_locations_worked",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_location_info = []
        for location_dict in add_healthcare_locations_worked:
            if not isinstance(location_dict, dict):
                rqst_errors.append('Error: A location object in \'add_healthcare_locations_worked\' is not a object.')
            else:
                location_info = {
                    "name": clean_string_value_from_dict_object(
                        location_dict,
                        "add_location_object",
                        'name',
                        rqst_errors
                    ),
                    "state_province": clean_string_value_from_dict_object(
                        location_dict,
                        "add_location_object",
                        'state_province',
                        rqst_errors,
                        none_allowed=True
                    )
                }
                if not location_info['state_province']:
                    location_info['state_province'] = 'not available'

                validated_location_info.append(location_info)

        validated_params['add_healthcare_locations_worked'] = validated_location_info
    elif 'remove_healthcare_locations_worked' in rqst_body:
        remove_healthcare_locations_worked = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "remove_healthcare_locations_worked",
            rqst_errors
        )

        validated_location_info = []
        for location_dict in remove_healthcare_locations_worked:
            if not isinstance(location_dict, dict):
                rqst_errors.append('Error: A location object in \'remove_healthcare_locations_worked\' is not a object.')
            else:
                location_info = {
                    "name": clean_string_value_from_dict_object(
                        location_dict,
                        "remove_location_object",
                        'name',
                        rqst_errors
                    ),
                    "state_province": clean_string_value_from_dict_object(
                        location_dict,
                        "remove_location_object",
                        'state_province',
                        rqst_errors,
                        none_allowed=True
                    )
                }
                if not location_info['state_province']:
                    location_info['state_province'] = 'not available'

                validated_location_info.append(location_info)

        validated_params['remove_healthcare_locations_worked'] = validated_location_info

    if 'add_healthcare_service_expertises' in rqst_body:
        add_healthcare_service_expertises = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "add_healthcare_service_expertises",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_service_expertise_info = []
        for service_expertise in add_healthcare_service_expertises:
            if not isinstance(service_expertise, str):
                rqst_errors.append('Error: A service_expertise in \'add_healthcare_service_expertises\' is not a string.')
                continue

            validated_service_expertise_info.append(service_expertise)

        validated_params['add_healthcare_service_expertises'] = validated_service_expertise_info
    elif 'remove_healthcare_service_expertises' in rqst_body:
        remove_healthcare_service_expertises = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "remove_healthcare_service_expertises",
            rqst_errors
        )

        validated_service_expertise_info = []
        for service_expertise in remove_healthcare_service_expertises:
            if not isinstance(service_expertise, str):
                rqst_errors.append('Error: A service_expertise in \'remove_healthcare_service_expertises\' is not a string.')
                continue

            validated_service_expertise_info.append(service_expertise)

        validated_params['remove_healthcare_service_expertises'] = validated_service_expertise_info

    if 'add_insurance_carrier_specialties' in rqst_body:
        add_insurance_carrier_specialties = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "add_insurance_carrier_specialties",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_insurance_carrier_info = []
        for carrier_dict in add_insurance_carrier_specialties:
            if not isinstance(carrier_dict, dict):
                rqst_errors.append('Error: An insurance_carrier object in \'add_insurance_carrier_specialties\' is not a object.')
            else:
                validated_carrier_info = {
                    "name": clean_string_value_from_dict_object(
                        carrier_dict,
                        "insurance_carrier_object",
                        'name',
                        rqst_errors,
                        empty_string_allowed=True
                    ),
                    "state_province": clean_string_value_from_dict_object(
                        carrier_dict,
                        "insurance_carrier_object",
                        'state_province',
                        rqst_errors,
                        empty_string_allowed=True
                    )
                }
                if not validated_carrier_info['state_province']:
                    validated_carrier_info['state_province'] = 'not available'

                validated_insurance_carrier_info.append(validated_carrier_info)

        validated_params['add_insurance_carrier_specialties'] = validated_insurance_carrier_info
    elif 'remove_insurance_carrier_specialties' in rqst_body:
        remove_insurance_carrier_specialties = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "remove_insurance_carrier_specialties",
            rqst_errors
        )

        validated_insurance_carrier_info = []
        for carrier_dict in remove_insurance_carrier_specialties:
            if not isinstance(carrier_dict, dict):
                rqst_errors.append('Error: An insurance_carrier object in \'remove_insurance_carrier_specialties\' is not a object.')
            else:
                validated_carrier_info = {
                    "name": clean_string_value_from_dict_object(
                        carrier_dict,
                        "insurance_carrier_object",
                        'name',
                        rqst_errors,
                        empty_string_allowed=True
                    ),
                    "state_province": clean_string_value_from_dict_object(
                        carrier_dict,
                        "insurance_carrier_object",
                        'state_province',
                        rqst_errors,
                        empty_string_allowed=True
                    )
                }
                if not validated_carrier_info['state_province']:
                    validated_carrier_info['state_province'] = 'not available'

                validated_insurance_carrier_info.append(validated_carrier_info)

        validated_params['remove_insurance_carrier_specialties'] = validated_insurance_carrier_info

    if "address_line_1" in rqst_body:
        address_line_1 = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "address_line_1",
            rqst_errors,
            empty_string_allowed=True
        )
        validated_params["address_line_1"] = address_line_1

    if "address_line_2" in rqst_body:
        address_line_2 = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "address_line_2",
            rqst_errors,
            empty_string_allowed=True
        )
        if address_line_2 is None:
            address_line_2 = ''
        validated_params["address_line_2"] = address_line_2

    if "city" in rqst_body:
        city = clean_string_value_from_dict_object(rqst_body, "root", "city", rqst_errors, empty_string_allowed=True)
        validated_params["city"] = city

    if "state_province" in rqst_body:
        state_province = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "state_province",
            rqst_errors,
            empty_string_allowed=True
        )
        validated_params["state_province"] = state_province

    if "zipcode" in rqst_body:
        zipcode = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "zipcode",
            rqst_errors,
            empty_string_allowed=True
        )
        validated_params["zipcode"] = zipcode

    if "phone" in rqst_body:
        phone = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "phone",
            rqst_errors,
            none_allowed=True
        )

        validated_params["phone"] = phone

    if "reported_region" in rqst_body:
        reported_region = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "reported_region",
            rqst_errors,
            none_allowed=True
        )

        validated_params["reported_region"] = reported_region

    if "video_link" in rqst_body:
        video_link = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "video_link",
            rqst_errors,
            none_allowed=True
        )
        if video_link:
            validate = URLValidator()
            try:
                validate(video_link)
            except ValidationError:
                rqst_errors.append("'video_link' is not a valid url. value is: {}".format(video_link))

        validated_params["video_link"] = video_link

    if "navigator_organization" in rqst_body:
        navigator_organization = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "navigator_organization",
            rqst_errors,
            none_allowed=True
        )

        validated_params["navigator_organization"] = navigator_organization

    validate_nav_signup_resume_params(rqst_body, validated_params, rqst_errors)


def validate_nav_signup_resume_params(rqst_body, validated_params, rqst_errors):
    if "create_resume_row" in rqst_body:
        resume_row_params = clean_dict_value_from_dict_object(
            rqst_body,
            "root",
            "create_resume_row",
            rqst_errors
        )

        validated_resume_row_params = {}
        if resume_row_params:
            validated_resume_row_params = validate_create_resume_row_params(
                resume_row_params,
                rqst_errors
            )

        validated_params['create_resume_row'] = validated_resume_row_params
    elif "update_resume_row" in rqst_body:
        resume_row_params = clean_dict_value_from_dict_object(
            rqst_body,
            "root",
            "update_resume_row",
            rqst_errors
        )

        validated_resume_row_params = {}
        if resume_row_params:
            validated_resume_row_params = validate_update_resume_row_params(
                resume_row_params,
                rqst_errors
            )

        validated_params['update_resume_row'] = validated_resume_row_params
    elif "delete_resume_row" in rqst_body:
        resume_row_params = clean_dict_value_from_dict_object(
            rqst_body,
            "root",
            "delete_resume_row",
            rqst_errors
        )

        validated_resume_row_params = {}
        if resume_row_params:
            validated_resume_row_params = validate_delete_resume_row_params(
                resume_row_params,
                rqst_errors
            )

        validated_params['delete_resume_row'] = validated_resume_row_params


def validate_create_resume_row_params(resume_row_params, rqst_errors):
    validated_resume_row_params = {
        'profile_description': clean_string_value_from_dict_object(
            resume_row_params,
            "create_resume_row",
            "profile_description",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        ),
    }

    if "create_education_rows" in resume_row_params:
        education_row_params = clean_list_value_from_dict_object(
            resume_row_params,
            "create_resume_row",
            "create_education_rows",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_education_row_params = []
        if education_row_params:
            for education_row_index, education_row_dict in enumerate(education_row_params):
                validated_education_row_dict = validate_create_education_row_params(
                    education_row_dict,
                    education_row_index,
                    rqst_errors
                )
                validated_education_row_params.append(validated_education_row_dict)

            validated_resume_row_params['create_education_rows'] = validated_education_row_params

    if "create_job_rows" in resume_row_params:
        job_row_params = clean_list_value_from_dict_object(
            resume_row_params,
            "create_resume_row",
            "create_job_rows",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_job_row_params = []
        if job_row_params:
            for job_row_index, job_row_dict in enumerate(job_row_params):
                validated_job_row_dict = validate_create_job_row_params(
                    job_row_dict,
                    job_row_index,
                    rqst_errors
                )
                validated_job_row_params.append(validated_job_row_dict)

            validated_resume_row_params['create_job_rows'] = validated_job_row_params

    return validated_resume_row_params


def validate_update_resume_row_params(resume_row_params, rqst_errors):
    validated_resume_row_params = {
        'id': clean_int_value_from_dict_object(
            resume_row_params,
            "update_resume_row",
            "id",
            rqst_errors
        )
    }

    if 'profile_description' in resume_row_params:
        validated_resume_row_params['profile_description'] = clean_string_value_from_dict_object(
            resume_row_params,
            "update_resume_row",
            "profile_description",
            rqst_errors,
            empty_string_allowed=True,
            none_allowed=True
        )

    if "create_education_rows" in resume_row_params:
        education_row_params = clean_list_value_from_dict_object(
            resume_row_params,
            "update_resume_row",
            "create_education_rows",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_education_row_params = []
        if education_row_params:
            for education_row_index, education_row_dict in enumerate(education_row_params):
                validated_education_row_dict = validate_create_education_row_params(
                    education_row_dict,
                    education_row_index,
                    rqst_errors
                )
                validated_education_row_params.append(validated_education_row_dict)

            validated_resume_row_params['create_education_rows'] = validated_education_row_params
    elif "update_education_rows" in resume_row_params:
        education_row_params = clean_list_value_from_dict_object(
            resume_row_params,
            "update_resume_row",
            "update_education_rows",
            rqst_errors
        )

        validated_education_row_params = []
        if education_row_params:
            for education_row_index, education_row_dict in enumerate(education_row_params):
                validated_education_row_dict = validate_update_education_row_params(
                    education_row_dict,
                    education_row_index,
                    rqst_errors
                )
                validated_education_row_params.append(validated_education_row_dict)

            validated_resume_row_params['update_education_rows'] = validated_education_row_params
    elif "delete_education_rows" in resume_row_params:
        education_row_params = clean_list_value_from_dict_object(
            resume_row_params,
            "update_resume_row",
            "delete_education_rows",
            rqst_errors
        )

        validated_education_row_params = []
        if education_row_params:
            for education_row_index, education_row_dict in enumerate(education_row_params):
                validated_education_row_dict = validate_delete_education_row_params(
                    education_row_dict,
                    education_row_index,
                    rqst_errors
                )
                validated_education_row_params.append(validated_education_row_dict)

            validated_resume_row_params['delete_education_rows'] = validated_education_row_params

    if "create_job_rows" in resume_row_params:
        job_row_params = clean_list_value_from_dict_object(
            resume_row_params,
            "update_resume_row",
            "create_job_rows",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_job_row_params = []
        if job_row_params:
            for job_row_index, job_row_dict in enumerate(job_row_params):
                validated_job_row_dict = validate_create_job_row_params(
                    job_row_dict,
                    job_row_index,
                    rqst_errors
                )
                validated_job_row_params.append(validated_job_row_dict)

            validated_resume_row_params['create_job_rows'] = validated_job_row_params
    elif "update_job_rows" in resume_row_params:
        job_row_params = clean_list_value_from_dict_object(
            resume_row_params,
            "update_resume_row",
            "update_job_rows",
            rqst_errors
        )

        validated_job_row_params = []
        if job_row_params:
            for job_row_index, job_row_dict in enumerate(job_row_params):
                validated_job_row_dict = validate_update_job_row_params(
                    job_row_dict,
                    job_row_index,
                    rqst_errors
                )
                validated_job_row_params.append(validated_job_row_dict)

            validated_resume_row_params['update_job_rows'] = validated_job_row_params
    elif "delete_job_rows" in resume_row_params:
        job_row_params = clean_list_value_from_dict_object(
            resume_row_params,
            "update_resume_row",
            "delete_job_rows",
            rqst_errors
        )

        validated_job_row_params = []
        if job_row_params:
            for job_row_index, job_row_dict in enumerate(job_row_params):
                validated_job_row_dict = validate_delete_job_row_params(
                    job_row_dict,
                    job_row_index,
                    rqst_errors
                )
                validated_job_row_params.append(validated_job_row_dict)

            validated_resume_row_params['delete_job_rows'] = validated_job_row_params

    return validated_resume_row_params


def validate_delete_resume_row_params(resume_row_params, rqst_errors):
    validated_resume_row_params = {
        'id': clean_int_value_from_dict_object(
            resume_row_params,
            "delete_resume_row",
            "id",
            rqst_errors
        )
    }

    return validated_resume_row_params


def validate_create_education_row_params(education_row_dict, education_row_index, rqst_errors):
    validated_education_row_dict = {
        'school': clean_string_value_from_dict_object(
            education_row_dict,
            "create_education_row[{}]".format(education_row_index),
            "school",
            rqst_errors,
        ),
        'major': clean_string_value_from_dict_object(
            education_row_dict,
            "create_education_row[{}]".format(education_row_index),
            "major",
            rqst_errors,
            none_allowed=True
        ),
        'degree_type': clean_string_value_from_dict_object(
            education_row_dict,
            "create_education_row[{}]".format(education_row_index),
            "degree_type",
            rqst_errors,
            none_allowed=True
        ),
    }

    if not validated_education_row_dict['degree_type']:
        validated_education_row_dict['degree_type'] = "Not Available"

    return validated_education_row_dict


def validate_update_education_row_params(education_row_dict, education_row_index, rqst_errors):
    validated_education_row_dict = {
        'id': clean_int_value_from_dict_object(
            education_row_dict,
            "update_education_row[{}]".format(education_row_index),
            "id",
            rqst_errors
        )
    }

    if 'school' in education_row_dict:
        validated_education_row_dict['school'] = clean_string_value_from_dict_object(
            education_row_dict,
            "update_education_row[{}]".format(education_row_index),
            "school",
            rqst_errors,
        )
    if 'major' in education_row_dict:
        validated_education_row_dict['major'] = clean_string_value_from_dict_object(
            education_row_dict,
            "update_education_row[{}]".format(education_row_index),
            "major",
            rqst_errors,
            none_allowed=True
        )
    if 'degree_type' in education_row_dict:
        validated_education_row_dict['degree_type'] = clean_string_value_from_dict_object(
            education_row_dict,
            "update_education_row[{}]".format(education_row_index),
            "degree_type",
            rqst_errors,
            none_allowed=True
        )
        if not validated_education_row_dict['degree_type']:
            validated_education_row_dict['degree_type'] = "Not Available"

    return validated_education_row_dict


def validate_delete_education_row_params(education_row_dict, education_row_index, rqst_errors):
    validated_education_row_dict = {
        'id': clean_int_value_from_dict_object(
            education_row_dict,
            "delete_education_row[{}]".format(education_row_index),
            "id",
            rqst_errors
        )
    }

    return validated_education_row_dict


def validate_create_job_row_params(job_row_dict, job_row_index, rqst_errors):
    validated_job_row_dict = {
        'title': clean_string_value_from_dict_object(
            job_row_dict,
            "create_job_row[{}]".format(job_row_index),
            "title",
            rqst_errors,
        ),
        'company': clean_string_value_from_dict_object(
            job_row_dict,
            "create_job_row[{}]".format(job_row_index),
            "company",
            rqst_errors,
        ),
        'description': clean_string_value_from_dict_object(
            job_row_dict,
            "create_job_row[{}]".format(job_row_index),
            "description",
            rqst_errors,
            none_allowed=True
        ),
    }

    return validated_job_row_dict


def validate_update_job_row_params(job_row_dict, job_row_index, rqst_errors):
    validated_job_row_dict = {
        'id': clean_int_value_from_dict_object(
            job_row_dict,
            "update_job_row[{}]".format(job_row_index),
            "id",
            rqst_errors
        )
    }

    if 'title' in job_row_dict:
        validated_job_row_dict['title'] = clean_string_value_from_dict_object(
            job_row_dict,
            "update_job_row[{}]".format(job_row_index),
            "title",
            rqst_errors,
        )
    if 'company' in job_row_dict:
        validated_job_row_dict['company'] = clean_string_value_from_dict_object(
            job_row_dict,
            "update_job_row[{}]".format(job_row_index),
            "company",
            rqst_errors,
        )
    if 'description' in job_row_dict:
        validated_job_row_dict['description'] = clean_string_value_from_dict_object(
            job_row_dict,
            "update_job_row[{}]".format(job_row_index),
            "description",
            rqst_errors,
            none_allowed=True
        )

    return validated_job_row_dict


def validate_delete_job_row_params(job_row_dict, job_row_index, rqst_errors):
    validated_job_row_dict = {
        'id': clean_int_value_from_dict_object(
            job_row_dict,
            "delete_job_row[{}]".format(job_row_index),
            "id",
            rqst_errors
        )
    }

    return validated_job_row_dict
