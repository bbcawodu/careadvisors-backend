from django.db import IntegrityError
import picmodels


def create_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_usr_email = validated_params['rqst_usr_email']
    usr_rqst_values = {
        "first_name": validated_params['rqst_usr_f_name'],
        "last_name": validated_params['rqst_usr_l_name'],
        "type": validated_params['rqst_usr_type'],
        "county": validated_params['rqst_county'],
        "mpn": validated_params['rqst_usr_mpn']
    }

    row, row_created = cls.objects.get_or_create(
        email=rqst_usr_email,
        defaults=usr_rqst_values
    )

    if not row_created:
        rqst_errors.append('Staff database entry already exists for the email: {!s}'.format(rqst_usr_email))
        row = None
    else:
        row.base_locations = validated_params['base_location_objects']
        row.save()
    update_nav_signup_columns_for_row(row, validated_params, rqst_errors)
    if rqst_errors:
        row.delete()
        row = None

    return row


def update_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_usr_id = validated_params['rqst_usr_id']
    rqst_usr_email = None

    try:
        row = cls.objects.get(id=rqst_usr_id)

        if 'rqst_usr_f_name' in validated_params:
            row.first_name = validated_params['rqst_usr_f_name']

        if 'rqst_usr_l_name' in validated_params:
            row.last_name = validated_params['rqst_usr_l_name']

        if 'rqst_usr_type' in validated_params:
            row.type = validated_params['rqst_usr_type']

        if 'rqst_county' in validated_params:
            row.county = validated_params['rqst_county']

        if 'rqst_usr_email' in validated_params:
            rqst_usr_email = validated_params['rqst_usr_email']
            row.email = rqst_usr_email
        else:
            rqst_usr_email = row.email

        if 'rqst_usr_mpn' in validated_params:
            row.mpn = validated_params['rqst_usr_mpn']

        update_nav_signup_columns_for_row(row, validated_params, rqst_errors)

        if not rqst_errors:
            if 'base_location_objects' in validated_params:
                row.base_locations.clear()
                row.base_locations = validated_params['base_location_objects']

        row.save()
    except cls.DoesNotExist:
        rqst_errors.append('Staff database entry does not exist for the id: {!s}'.format(str(rqst_usr_id)))
        row = None
    except cls.MultipleObjectsReturned:
        rqst_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_usr_id)))
        row = None
    except IntegrityError:
        rqst_errors.append('Database entry already exists for the email: {!s}'.format(rqst_usr_email))
        row = None

    return row


def delete_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_usr_id = validated_params['rqst_usr_id']

    try:
        staff_instance = cls.objects.get(id=rqst_usr_id)
        staff_instance.delete()
    except cls.DoesNotExist:
        rqst_errors.append('Staff database entry does not exist for the id: {!s}'.format(str(rqst_usr_id)))
    except cls.MultipleObjectsReturned:
        rqst_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_usr_id)))


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
                get_provider_location_row_with_given_name_and_state(service_expertise, rqst_errors)
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
                get_provider_location_row_with_given_name_and_state(service_expertise, rqst_errors)
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

    modify_row_address()
    if "phone" in validated_params:
        row.phone = validated_params['phone']
    if "reported_region" in validated_params:
        row.reported_region = validated_params['reported_region']
    if "video_link" in validated_params:
        row.video_link = validated_params['video_link']

    if not rqst_errors:
        row.save()


def get_service_expertise_row_with_given_name(name, rqst_errors):
    row = None

    if name:
        try:
            row = picmodels.models.HealthcareServiceExpertise.objects.get(name__iexact=name)
        except picmodels.models.HealthcareServiceExpertise.DoesNotExist:
            row = None
            rqst_errors.append("No HealthcareServiceExpertise row found with name: {}".format(name))

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
                "Healthcare location with the name: {} and state: {} does not exist in row id {}'s healthcare_locations_used list (Hint - remove from parameter 'add_healthcare_locations_used' list)".format(
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
                "service_expertise with the name: {} does not exists in row id {}'s service_expertise list (Hint - remove from parameter 'add_healthcare_service_expertises' list)".format(
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
                "insurance_carrier with the name: {} and state: {} does not exists in row id {}'s insurance_carrier_specialties list (Hint - remove from parameter 'add_insurance_carrier_specialties' list)".format(
                    insurance_carrier.name,
                    insurance_carrier.state_province,
                    row.id,
                )
            )
