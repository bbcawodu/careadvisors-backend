from django.db import IntegrityError
import picmodels


def create_row_w_validated_params(cls, validated_params, rqst_errors):
    email = validated_params['email']
    usr_rqst_values = {
        "first_name": validated_params['first_name'],
        "last_name": validated_params['last_name'],
        "type": validated_params['type'],
        "county": validated_params['county'],
        "mpn": validated_params['mpn']
    }

    row, row_created = cls.objects.get_or_create(
        email=email,
        defaults=usr_rqst_values
    )

    if not row_created:
        rqst_errors.append('Navigator database entry already exists for the email: {!s}'.format(email))
        row = None
    else:
        row.save()

        if 'add_base_locations' in validated_params:
            base_location_names = validated_params['add_base_locations']
            base_location_rows = []
            for base_location_name in base_location_names:
                base_location_rows.append(
                    get_nav_metrics_location_row_with_given_name(base_location_name, rqst_errors)
                )
            if not rqst_errors:
                check_base_locations_for_given_rows(
                    row.base_locations.all(),
                    base_location_rows,
                    row,
                    rqst_errors
                )
                if not rqst_errors:
                    for base_location_row in base_location_rows:
                        row.base_locations.add(base_location_row)

        update_nav_signup_columns_for_row(row, validated_params, rqst_errors)
        if rqst_errors:
            row.delete()
            row = None

    return row


def update_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['id']
    email = None

    try:
        row = cls.objects.get(id=rqst_id)

        if 'first_name' in validated_params:
            row.first_name = validated_params['first_name']

        if 'last_name' in validated_params:
            row.last_name = validated_params['last_name']

        if 'type' in validated_params:
            row.type = validated_params['type']

        if 'county' in validated_params:
            row.county = validated_params['county']

        if 'email' in validated_params:
            email = validated_params['email']
            row.email = email
        else:
            email = row.email

        if 'mpn' in validated_params:
            row.mpn = validated_params['mpn']

        if 'add_base_locations' in validated_params:
            base_location_names = validated_params['add_base_locations']
            base_location_rows = []
            for base_location_name in base_location_names:
                base_location_rows.append(
                    get_nav_metrics_location_row_with_given_name(base_location_name, rqst_errors)
                )
            if not rqst_errors:
                check_base_locations_for_given_rows(
                    row.base_locations.all(),
                    base_location_rows,
                    row,
                    rqst_errors
                )
                if not rqst_errors:
                    for base_location_row in base_location_rows:
                        row.base_locations.add(base_location_row)
        elif 'remove_base_locations' in validated_params:
            base_location_names = validated_params['remove_base_locations']
            base_location_rows = []
            for base_location_name in base_location_names:
                base_location_rows.append(
                    get_nav_metrics_location_row_with_given_name(base_location_name, rqst_errors)
                )
            if not rqst_errors:
                check_base_locations_for_not_given_rows(
                    row.base_locations.all(),
                    base_location_rows,
                    row,
                    rqst_errors
                )
                if not rqst_errors:
                    for base_location_row in base_location_rows:
                        row.base_locations.remove(base_location_row)

        if not rqst_errors:
            update_nav_signup_columns_for_row(row, validated_params, rqst_errors)

        row.save()
    except cls.DoesNotExist:
        rqst_errors.append('Navigator database row does not exist for the id: {!s}'.format(str(rqst_id)))
        row = None
    except cls.MultipleObjectsReturned:
        rqst_errors.append('Multiple database rows exist for the id: {!s}'.format(str(rqst_id)))
        row = None
    except IntegrityError:
        rqst_errors.append('Database row already exists for the email: {!s}'.format(email))
        row = None

    return row


def delete_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['id']

    try:
        staff_instance = cls.objects.get(id=rqst_id)
        staff_instance.delete()
    except cls.DoesNotExist:
        rqst_errors.append('Staff database entry does not exist for the id: {!s}'.format(str(rqst_id)))
    except cls.MultipleObjectsReturned:
        rqst_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_id)))


def update_nav_signup_columns_for_row(row, validated_params, rqst_errors):
    def modify_row_address():
        address_instance = row.address
        if address_instance:
            if 'address_line_1' in validated_params:
                address_instance.address_line_1 = validated_params['address_line_1']
            if 'address_line_2' in validated_params:
                address_instance.address_line_2 = validated_params['address_line_2']
            if 'city' in validated_params:
                address_instance.city = validated_params['city']
            if 'state_province' in validated_params:
                address_instance.state_province = validated_params['state_province']
            if 'zipcode' in validated_params:
                address_instance.zipcode = validated_params['zipcode']
        else:
            there_are_any_address_fields_in_validated_params = 'address_line_1' in validated_params or \
                                                               'city' in validated_params or \
                                                               'state_province' in validated_params or \
                                                               'zipcode' in validated_params or \
                                                               'address_line_2' in validated_params
            if there_are_any_address_fields_in_validated_params:
                there_are_enough_fields_to_create_address_instance = 'address_line_1' in validated_params and \
                                                                     'city' in validated_params and \
                                                                     'state_province' in validated_params and \
                                                                     'zipcode' in validated_params
                if there_are_enough_fields_to_create_address_instance:
                    if 'address_line_2' not in validated_params:
                        validated_params['address_line_2'] = ''
                    required_address_fields_are_not_empty_strings = validated_params['address_line_1'] != '' and \
                                                                    validated_params['city'] != '' and \
                                                                    validated_params['state_province'] != '' and \
                                                                    validated_params['zipcode'] != ''

                    if required_address_fields_are_not_empty_strings:
                        address_instance, address_instance_created = picmodels.models.Address.objects.get_or_create(
                            address_line_1=validated_params['address_line_1'],
                            address_line_2=validated_params['address_line_2'],
                            city=validated_params['city'],
                            state_province=validated_params['state_province'],
                            zipcode=validated_params['zipcode'],
                            country=picmodels.models.Country.objects.all()[0])

                        row.address = address_instance
                # else:
                #     rqst_errors.append("There are not enough fields to create an address instance.")

    if 'add_healthcare_locations_worked' in validated_params:
        healthcare_location_info = validated_params['add_healthcare_locations_worked']
        healthcare_location_rows = []
        for location_dict in healthcare_location_info:
            healthcare_location_rows.append(get_provider_location_row_with_given_name_and_state(location_dict, rqst_errors))
        if not rqst_errors:
            check_healthcare_locations_worked_for_given_rows(
                row.healthcare_locations_worked.all(),
                healthcare_location_rows,
                row,
                rqst_errors
            )
            if not rqst_errors:
                for location_row in healthcare_location_rows:
                    row.healthcare_locations_worked.add(location_row)
    elif 'remove_healthcare_locations_worked' in validated_params:
        healthcare_location_info = validated_params['remove_healthcare_locations_worked']
        healthcare_location_rows = []
        for location_dict in healthcare_location_info:
            healthcare_location_rows.append(
                get_provider_location_row_with_given_name_and_state(location_dict, rqst_errors))
        if not rqst_errors:
            check_healthcare_locations_worked_for_not_given_rows(
                row.healthcare_locations_worked.all(),
                healthcare_location_rows,
                row,
                rqst_errors
            )
            if not rqst_errors:
                for location_row in healthcare_location_rows:
                    row.healthcare_locations_worked.remove(location_row)

    if 'add_healthcare_service_expertises' in validated_params:
        service_expertise_info = validated_params['add_healthcare_service_expertises']
        service_expertise_rows = []
        for service_expertise in service_expertise_info:
            service_expertise_rows.append(
                get_service_expertise_row_with_given_name(service_expertise, rqst_errors)
            )
        if not rqst_errors:
            check_service_expertises_for_given_rows(
                row.healthcare_service_expertises.all(),
                service_expertise_rows,
                row,
                rqst_errors
            )
            if not rqst_errors:
                for service_expertise in service_expertise_rows:
                    row.healthcare_service_expertises.add(service_expertise)
    elif 'remove_healthcare_service_expertises' in validated_params:
        service_expertise_info = validated_params['remove_healthcare_service_expertises']
        service_expertise_rows = []
        for service_expertise in service_expertise_info:
            service_expertise_rows.append(
                get_service_expertise_row_with_given_name(service_expertise, rqst_errors)
            )
        if not rqst_errors:
            check_service_expertises_for_not_given_rows(
                row.healthcare_service_expertises.all(),
                service_expertise_rows,
                row,
                rqst_errors
            )
            if not rqst_errors:
                for service_expertise in service_expertise_rows:
                    row.healthcare_service_expertises.remove(service_expertise)

    if 'add_insurance_carrier_specialties' in validated_params:
        insurance_carrier_info = validated_params['add_insurance_carrier_specialties']
        insurance_carrier_rows = []
        for insurance_carrier_dict in insurance_carrier_info:
            insurance_carrier_rows.append(
                get_carrier_row_with_given_name_and_state(insurance_carrier_dict, rqst_errors)
            )
        if not rqst_errors:
            check_insurance_carrier_specialties_for_given_rows(
                row.insurance_carrier_specialties.all(),
                insurance_carrier_rows,
                row,
                rqst_errors
            )
            if not rqst_errors:
                for insurance_carrier in insurance_carrier_rows:
                    row.insurance_carrier_specialties.add(insurance_carrier)
    elif 'remove_insurance_carrier_specialties' in validated_params:
        insurance_carrier_info = validated_params['remove_insurance_carrier_specialties']
        insurance_carrier_rows = []
        for insurance_carrier_dict in insurance_carrier_info:
            insurance_carrier_rows.append(
                get_carrier_row_with_given_name_and_state(insurance_carrier_dict, rqst_errors)
            )
        if not rqst_errors:
            check_insurance_carrier_specialties_for_not_given_rows(
                row.insurance_carrier_specialties.all(),
                insurance_carrier_rows,
                row,
                rqst_errors
            )
            if not rqst_errors:
                for insurance_carrier in insurance_carrier_rows:
                    row.insurance_carrier_specialties.remove(insurance_carrier)

    if not rqst_errors:
        modify_row_address()
        manage_nav_resume_table_row_for_row(row, validated_params, rqst_errors)

        if "phone" in validated_params:
            row.phone = validated_params['phone']
        if "reported_region" in validated_params:
            row.reported_region = validated_params['reported_region']
        if "video_link" in validated_params:
            row.video_link = validated_params['video_link']
        if "navigator_organization" in validated_params:
            row.navigator_organization = validated_params['navigator_organization']

        if not rqst_errors:
            row.save()


def manage_nav_resume_table_row_for_row(row, validated_params, rqst_errors):
    if 'create_resume_row' in validated_params:
        create_resume_row_params = validated_params['create_resume_row']
        create_resume_row_w_validated_params(row, create_resume_row_params, rqst_errors)
    elif 'update_resume_row' in validated_params:
        update_resume_row_params = validated_params['update_resume_row']
        update_resume_row_w_validated_params(row, update_resume_row_params, rqst_errors)
    elif 'delete_resume_row' in validated_params:
        delete_resume_row_params = validated_params['delete_resume_row']
        delete_resume_row_w_validated_params(delete_resume_row_params, rqst_errors)


def create_resume_row_w_validated_params(nav_row, resume_row_params, rqst_errors):
    resume_row = picmodels.models.Resume(
        navigator=nav_row,
        profile_description=resume_row_params['profile_description']
    )
    resume_row.save()

    education_rows = []
    job_rows = []
    if "create_education_rows" in resume_row_params:
        create_education_row_params = resume_row_params["create_education_rows"]
        for education_row_dict in create_education_row_params:
            education_rows.append(create_education_row_w_validated_params(resume_row, education_row_dict, rqst_errors))

    if not rqst_errors:
        if "create_job_rows" in resume_row_params:
            create_job_row_params = resume_row_params["create_job_rows"]
            for job_row_dict in create_job_row_params:
                job_rows.append(create_job_row_w_validated_params(resume_row, job_row_dict))

    if not rqst_errors:
        resume_row.save()
        for row in education_rows:
            row.save()
        for row in job_rows:
            row.save()
    else:
        resume_row.delete()


def update_resume_row_w_validated_params(nav_row, resume_row_params, rqst_errors):
    try:
        resume_row = picmodels.models.Resume.objects.get(id=resume_row_params['id'])
        resume_row.navigator = nav_row
    except picmodels.models.Resume.DoesNotExist:
        resume_row = None
        rqst_errors.append("No Resume row found with id: {}".format(resume_row_params['id']))

    if resume_row:
        education_rows = []
        job_rows = []

        if "create_education_rows" in resume_row_params:
            create_education_row_params = resume_row_params["create_education_rows"]
            for education_row_dict in create_education_row_params:
                education_rows.append(create_education_row_w_validated_params(resume_row, education_row_dict, rqst_errors))
        elif "update_education_rows" in resume_row_params:
            update_education_row_params = resume_row_params["update_education_rows"]
            for education_row_dict in update_education_row_params:
                education_rows.append(update_education_row_w_validated_params(resume_row, education_row_dict, rqst_errors))
        elif "delete_education_rows" in resume_row_params:
            delete_education_row_params = resume_row_params["delete_education_rows"]
            for education_row_dict in delete_education_row_params:
                delete_education_row_w_validated_params(education_row_dict, rqst_errors)

        if not rqst_errors:
            if "create_job_rows" in resume_row_params:
                create_job_row_params = resume_row_params["create_job_rows"]
                for job_row_dict in create_job_row_params:
                    job_rows.append(create_job_row_w_validated_params(resume_row, job_row_dict))
            elif "job_education_rows" in resume_row_params:
                update_job_row_params = resume_row_params["update_job_rows"]
                for job_row_dict in update_job_row_params:
                    job_rows.append(update_job_row_w_validated_params(resume_row, job_row_dict, rqst_errors))
            elif "delete_job_rows" in resume_row_params:
                delete_job_row_params = resume_row_params["delete_job_rows"]
                for job_row_dict in delete_job_row_params:
                    delete_job_row_w_validated_params(job_row_dict, rqst_errors)

        if not rqst_errors:
            if "profile_description" in resume_row_params:
                resume_row.profile_description = resume_row_params['profile_description']

            resume_row.save()

            for row in education_rows:
                row.save()
            for row in job_rows:
                row.save()


def delete_resume_row_w_validated_params(resume_row_params, rqst_errors):
    try:
        resume_row = picmodels.models.Resume.objects.get(id=resume_row_params['id'])
    except picmodels.models.Resume.DoesNotExist:
        resume_row = None
        rqst_errors.append("No Resume row found with id: {}".format(resume_row_params['id']))

    if resume_row:
        resume_row.delete()


def create_education_row_w_validated_params(resume_row, education_row_dict, rqst_errors):
    education_row = picmodels.models.Education(resume=resume_row)
    education_row.school = education_row_dict['school']
    education_row.major = education_row_dict['major']
    education_row.degree_type = education_row_dict['degree_type']
    if not education_row.check_degree_type_choices():
        rqst_errors.append(
            "degree_type: {!s} is not a valid choice".format(education_row.degree_type)
        )
    if "start_year_datetime" in education_row_dict:
        education_row.start_date = education_row_dict['start_year_datetime']
    if "end_year_datetime" in education_row_dict:
        education_row.end_date = education_row_dict['end_year_datetime']

    return education_row


def update_education_row_w_validated_params(resume_row, education_row_dict, rqst_errors):
    try:
        education_row = picmodels.models.Education.objects.get(id=education_row_dict['id'])
        education_row.resume = resume_row
    except picmodels.models.Education.DoesNotExist:
        education_row = None
        rqst_errors.append("No Education row found with id: {}".format(education_row_dict['id']))

    if education_row:
        if 'school' in education_row_dict:
            education_row.school = education_row_dict['school']
        if 'major' in education_row_dict:
            education_row.major = education_row_dict['major']
        if 'degree_type' in education_row_dict:
            education_row.degree_type = education_row_dict['degree_type']
            if not education_row.check_degree_type_choices():
                rqst_errors.append(
                    "degree_type: {!s} is not a valid choice".format(education_row.degree_type)
                )
        if "start_year_datetime" in education_row_dict:
            education_row.start_date = education_row_dict['start_year_datetime']
        if "end_year_datetime" in education_row_dict:
            education_row.end_date = education_row_dict['end_year_datetime']

    return education_row


def delete_education_row_w_validated_params(education_row_dict, rqst_errors):
    try:
        education_row = picmodels.models.Education.objects.get(id=education_row_dict['id'])
    except picmodels.models.Education.DoesNotExist:
        education_row = None
        rqst_errors.append("No Education row found with id: {}".format(education_row_dict['id']))

    if education_row:
        education_row.delete()


def create_job_row_w_validated_params(resume_row, job_row_dict):
    job_row = picmodels.models.Job(resume=resume_row)
    job_row.title = job_row_dict['title']
    job_row.company = job_row_dict['company']
    job_row.description = job_row_dict['description']
    if "start_year_datetime" in job_row_dict:
        job_row.start_date = job_row_dict['start_year_datetime']
    if "end_year_datetime" in job_row_dict:
        job_row.end_date = job_row_dict['end_year_datetime']

    return job_row


def update_job_row_w_validated_params(resume_row, job_row_dict, rqst_errors):
    try:
        job_row = picmodels.models.Job.objects.get(id=job_row_dict['id'])
        job_row.resume = resume_row
    except picmodels.models.Job.DoesNotExist:
        job_row = None
        rqst_errors.append("No Job row found with id: {}".format(job_row_dict['id']))

    if job_row:
        if 'title' in job_row_dict:
            job_row.title = job_row_dict['title']
        if 'company' in job_row_dict:
            job_row.company = job_row_dict['company']
        if 'description' in job_row_dict:
            job_row.description = job_row_dict['description']
        if "start_year_datetime" in job_row_dict:
            job_row.start_date = job_row_dict['start_year_datetime']
        if "end_year_datetime" in job_row_dict:
            job_row.end_date = job_row_dict['end_year_datetime']

    return job_row


def delete_job_row_w_validated_params(job_row_dict, rqst_errors):
    try:
        job_row = picmodels.models.Job.objects.get(id=job_row_dict['id'])
    except picmodels.models.Job.DoesNotExist:
        job_row = None
        rqst_errors.append("No Job row found with id: {}".format(job_row_dict['id']))

    if job_row:
        job_row.delete()


def get_service_expertise_row_with_given_name(name, rqst_errors):
    row = None

    if name:
        try:
            row = picmodels.models.HealthcareServiceExpertise.objects.get(name__iexact=name)
        except picmodels.models.HealthcareServiceExpertise.DoesNotExist:
            row = None
            rqst_errors.append("No HealthcareServiceExpertise row found with name: {}".format(name))

    return row


def get_nav_metrics_location_row_with_given_name(name, rqst_errors):
    row = None

    if name:
        try:
            row = picmodels.models.NavMetricsLocation.objects.get(name__iexact=name)
        except picmodels.models.NavMetricsLocation.DoesNotExist:
            row = None
            rqst_errors.append("No NavMetricsLocation row found with name: {}".format(name))

    return row


def get_carrier_row_with_given_name_and_state(validated_params, rqst_errors):
    row = None
    name = validated_params['name']
    state = validated_params['state_province']

    if name:
        try:
            row = picmodels.models.HealthcareCarrier.objects.get(name__iexact=name, state_province__iexact=state)
        except picmodels.models.HealthcareCarrier.DoesNotExist:
            row = None
            rqst_errors.append("No HealthcareCarrier row found with name: {} and state: {}".format(name, state))

    return row


def get_provider_location_row_with_given_name_and_state(location_dict, rqst_errors):
    row = None

    if location_dict:
        try:
            row = picmodels.models.ProviderLocation.objects.get(
                name__iexact=location_dict['name'],
                state_province__iexact=location_dict['state_province']
            )
        except picmodels.models.ProviderLocation.DoesNotExist:
            row = None
            rqst_errors.append(
                "No ProviderLocation row found with name: {} and state: {}".format(
                    location_dict['name'],
                    location_dict['state_province']
                )
            )

    return row


def check_healthcare_locations_worked_for_given_rows(cur_locations_used_qset, given_locations_used_list, consumer_row, rqst_errors):
    for location_used in given_locations_used_list:
        if location_used in cur_locations_used_qset:
            rqst_errors.append(
                "Healthcare location with the name: {} and state: {} already exists in row id {}'s healthcare_locations_used list (Hint - remove from parameter 'add_healthcare_locations_used' list)".format(
                    location_used.name,
                    location_used.state_province,
                    consumer_row.id,
                )
            )


def check_healthcare_locations_worked_for_not_given_rows(cur_locations_used_qset, given_locations_used_list, consumer_row, rqst_errors):
    for location_used in given_locations_used_list:
        if location_used not in cur_locations_used_qset:
            rqst_errors.append(
                "Healthcare location with the name: {} and state: {} does not exist in row id {}'s healthcare_locations_used list (Hint - remove from parameter 'remove_healthcare_locations_used' list)".format(
                    location_used.name,
                    location_used.state_province,
                    consumer_row.id,
                )
            )


def check_service_expertises_for_given_rows(cur_service_expertise_qset, given_service_expertise_list, row, rqst_errors):
    for service_expertise in given_service_expertise_list:
        if service_expertise in cur_service_expertise_qset:
            rqst_errors.append(
                "service_expertise with the name: {} already exists in row id {}'s service_expertise list (Hint - remove from parameter 'add_healthcare_service_expertises' list)".format(
                    service_expertise.name,
                    row.id,
                )
            )


def check_service_expertises_for_not_given_rows(cur_service_expertise_qset, given_service_expertise_list, row, rqst_errors):
    for service_expertise in given_service_expertise_list:
        if service_expertise not in cur_service_expertise_qset:
            rqst_errors.append(
                "service_expertise with the name: {} does not exists in row id {}'s service_expertise list (Hint - remove from parameter 'remove_healthcare_service_expertises' list)".format(
                    service_expertise.name,
                    row.id,
                )
            )


def check_insurance_carrier_specialties_for_given_rows(cur_insurance_carrier_specialties_qset, given_insurance_carrier_list, row, rqst_errors):
    for insurance_carrier in given_insurance_carrier_list:
        if insurance_carrier in cur_insurance_carrier_specialties_qset:
            rqst_errors.append(
                "insurance_carrier with the name: {} and state: {} already exists in row id {}'s insurance_carrier_specialties list (Hint - remove from parameter 'add_insurance_carrier_specialties' list)".format(
                    insurance_carrier.name,
                    insurance_carrier.state_province,
                    row.id,
                )
            )


def check_insurance_carrier_specialties_for_not_given_rows(cur_insurance_carrier_specialties_qset, given_insurance_carrier_list, row, rqst_errors):
    for insurance_carrier in given_insurance_carrier_list:
        if insurance_carrier not in cur_insurance_carrier_specialties_qset:
            rqst_errors.append(
                "insurance_carrier with the name: {} and state: {} does not exists in row id {}'s insurance_carrier_specialties list (Hint - remove from parameter 'remove_insurance_carrier_specialties' list)".format(
                    insurance_carrier.name,
                    insurance_carrier.state_province,
                    row.id,
                )
            )


def check_base_locations_for_given_rows(cur_base_locations_qset, given_nav_metrics_locations_list, row, rqst_errors):
    for nav_metrics_location in given_nav_metrics_locations_list:
        if nav_metrics_location in cur_base_locations_qset:
            rqst_errors.append(
                "nav_metrics_location with the name: {} already exists in row id {}'s base_locations list (Hint - remove from parameter 'add_base_locations' list)".format(
                    nav_metrics_location.name,
                    row.id,
                )
            )


def check_base_locations_for_not_given_rows(cur_base_locations_qset, given_nav_metrics_locations_list, row, rqst_errors):
    for nav_metrics_location in given_nav_metrics_locations_list:
        if nav_metrics_location not in cur_base_locations_qset:
            rqst_errors.append(
                "nav_metrics_location with the name: {} does not exists in row id {}'s base_locations list (Hint - remove from parameter 'remove_base_locations' list)".format(
                    nav_metrics_location.name,
                    row.id,
                )
            )
