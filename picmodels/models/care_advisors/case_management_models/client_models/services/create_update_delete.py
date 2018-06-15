import picmodels


def create_row_w_validated_params(cls, validated_params, rqst_errors):
    if 'name' not in validated_params:
        rqst_errors.append("'name' is a required key in the validated_params argument")
        return None

    row = cls()

    modify_row_address(row, validated_params)
    row.name = validated_params['name']

    if not cls.check_for_rows_with_given_name_and_address(row.name, row.address, rqst_errors):
        if not rqst_errors:
            row.save()

        if 'add_cm_sequences' in validated_params:
            cm_sequence_ids = validated_params['add_cm_sequences']
            cm_sequence_rows = []
            for cm_sequence_id in cm_sequence_ids:
                cm_sequence_rows.append(
                    get_case_management_sequences_row_with_given_id(cm_sequence_id, rqst_errors)
                )
            if not rqst_errors:
                check_cm_sequences_for_given_rows(
                    row.cm_sequences.all(),
                    cm_sequence_rows,
                    row,
                    rqst_errors
                )
                if not rqst_errors:
                    for cm_sequence_row in cm_sequence_rows:
                        row.cm_sequences.add(cm_sequence_row)

        if not rqst_errors:
            row.save()
        else:
            row.delete()
            row = None

    return row


def update_row_w_validated_params(cls, validated_params, rqst_errors):
    if 'id' not in validated_params:
        rqst_errors.append("'id' is a required key in the validated_params argument")
        return None

    rqst_id = validated_params['id']

    try:
        row = cls.objects.get(id=rqst_id)
    except cls.DoesNotExist:
        rqst_errors.append('Row does not exist for the id: {}'.format(rqst_id))
        return None

    if 'name' in validated_params:
        row.name = validated_params['name']

    modify_row_address(row, validated_params)

    if not cls.check_for_rows_with_given_name_and_address(row.name, row.address, rqst_errors, rqst_id):
        if 'add_cm_sequences' in validated_params:
            cm_sequence_ids = validated_params['add_cm_sequences']
            cm_sequence_rows = []
            for cm_sequence_id in cm_sequence_ids:
                cm_sequence_rows.append(
                    get_case_management_sequences_row_with_given_id(cm_sequence_id, rqst_errors)
                )
            if not rqst_errors:
                check_cm_sequences_for_given_rows(
                    row.cm_sequences.all(),
                    cm_sequence_rows,
                    row,
                    rqst_errors
                )
                if not rqst_errors:
                    for cm_sequence_row in cm_sequence_rows:
                        row.cm_sequences.add(cm_sequence_row)
        elif 'remove_cm_sequences' in validated_params:
            cm_sequence_ids = validated_params['remove_cm_sequences']
            cm_sequence_rows = []
            for cm_sequence_id in cm_sequence_ids:
                cm_sequence_rows.append(
                    get_case_management_sequences_row_with_given_id(cm_sequence_id, rqst_errors)
                )
            if not rqst_errors:
                check_cm_sequences_for_not_given_rows(
                    row.cm_sequences.all(),
                    cm_sequence_rows,
                    row,
                    rqst_errors
                )
                if not rqst_errors:
                    for cm_sequence_row in cm_sequence_rows:
                        row.cm_sequences.remove(cm_sequence_row)

        if not rqst_errors:
            row.save()

    return row


def delete_row_w_validated_params(cls, validated_params, rqst_errors):
    if 'id' not in validated_params:
        rqst_errors.append("'id' is a required key in the validated_params argument")
        return

    rqst_id = validated_params['id']

    try:
        row = cls.objects.get(id=rqst_id)
        row.delete()
    except cls.DoesNotExist:
        rqst_errors.append('Row does not exist for the id: {!s}'.format(str(rqst_id)))


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


def check_for_rows_with_given_name_and_address(cls, name, address_row, rqst_errors, current_id=None):
    found_matching_rows = False

    matching_rows = cls.objects.filter(
        name__iexact=name,
        address=address_row
    )

    if matching_rows:
        found_matching_rows = True

        row_ids = []
        len_of_row_qset = len(matching_rows)
        for row in matching_rows:
            row_ids.append(row.id)

        if len_of_row_qset > 1:
            rqst_errors.append(
                "Multiple rows with name: {}, and address: {} already exist in db. (Hint - Delete all but one and modify the remaining) id's: {}".format(
                    name, address_row.return_values_dict() if address_row else address_row, row_ids))
        else:
            if not current_id or current_id not in row_ids:
                rqst_errors.append(
                    "Row with name: {}, and address: {} already exists in db. (Hint - Modify that entry) id: {}".format(
                        name, address_row.return_values_dict() if address_row else address_row, row_ids[0]))
            else:
                found_matching_rows = False

    return found_matching_rows


def get_case_management_sequences_row_with_given_id(sequence_id, rqst_errors):
    row = None

    if sequence_id:
        try:
            row = picmodels.models.CMSequences.objects.get(id=sequence_id)
        except picmodels.models.CMSequences.DoesNotExist:
            row = None
            rqst_errors.append("No CMSequences row found with id: {}".format(sequence_id))

    return row


def check_cm_sequences_for_given_rows(cur_cm_sequences, given_cm_sequences, row, rqst_errors):
    for cm_sequence in given_cm_sequences:
        if cm_sequence in cur_cm_sequences:
            rqst_errors.append(
                "cm_sequence with id: {} already exists in row id {}'s cm_sequences list (Hint - remove from parameter 'add_cm_sequences' list)".format(
                    cm_sequence.id,
                    row.id,
                )
            )


def check_cm_sequences_for_not_given_rows(cur_cm_sequences, given_cm_sequences, row, rqst_errors):
    for cm_sequence in given_cm_sequences:
        if cm_sequence not in cur_cm_sequences:
            rqst_errors.append(
                "cm_sequence with id: {} already exists in row id {}'s cm_sequences list (Hint - remove from parameter 'remove_cm_sequences' list)".format(
                    cm_sequence.id,
                    row.id,
                )
            )
