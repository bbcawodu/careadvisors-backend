import picmodels


def create_row_w_validated_params(cls, validated_params, rqst_errors):
    row = cls()

    company_name = validated_params['company_name']
    row.company_name = company_name

    modify_row_address(row, validated_params)

    estimated_monthly_caseload = validated_params['estimated_monthly_caseload']
    row.estimated_monthly_caseload = estimated_monthly_caseload

    contact_first_name = validated_params['contact_first_name']
    row.contact_first_name = contact_first_name

    contact_last_name = validated_params['contact_last_name']
    row.contact_last_name = contact_last_name

    contact_email = validated_params['contact_email']
    row.contact_email = contact_email

    contact_phone = validated_params['contact_phone']
    row.contact_phone = contact_phone

    appointment_datetime = validated_params['appointment_datetime']
    row.appointment_datetime = appointment_datetime

    if not rqst_errors:
        row.save()

    return row


def update_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['id']
    try:
        row = cls.objects.get(id=rqst_id)
    except cls.DoesNotExist:
        rqst_errors.append('Row in NavOrgsFromOnlineForm table does not exist for the id: {}'.format(rqst_id))
        row = None

    if row:
        if 'company_name' in validated_params:
            row.company_name = validated_params['company_name']

        modify_row_address(row, validated_params)

        if "estimated_monthly_caseload" in validated_params:
            estimated_monthly_caseload = validated_params['estimated_monthly_caseload']
            row.estimated_monthly_caseload = estimated_monthly_caseload

        if "contact_first_name" in validated_params:
            contact_first_name = validated_params['contact_first_name']
            row.contact_first_name = contact_first_name

        if "contact_last_name" in validated_params:
            contact_last_name = validated_params['contact_last_name']
            row.contact_last_name = contact_last_name

        if "contact_email" in validated_params:
            contact_email = validated_params['contact_email']
            row.contact_email = contact_email

        if "contact_phone" in validated_params:
            contact_phone = validated_params['contact_phone']
            row.contact_phone = contact_phone

        if "appointment_datetime" in validated_params:
            appointment_datetime = validated_params['appointment_datetime']
            row.appointment_datetime = appointment_datetime

        if not rqst_errors:
            row.save()

    return row


def delete_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['id']
    try:
        row = cls.objects.get(id=rqst_id)
        row.delete()
    except cls.DoesNotExist:
        rqst_errors.append('Row in NavOrgsFromOnlineForm table does not exist for the id: {}'.format(rqst_id))


def modify_row_address(row, validated_params):
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
