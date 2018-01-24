from django.db import IntegrityError


def create_staff_row_using_validated_params(cls, validated_params, rqst_errors):
    rqst_usr_email = validated_params['rqst_usr_email']
    usr_rqst_values = {
        "email": rqst_usr_email,
        "first_name": validated_params['rqst_usr_f_name'],
        "last_name": validated_params['rqst_usr_l_name'],
        "type": validated_params['rqst_usr_type'],
        "county": validated_params['rqst_county']
    }
    staff_instance, staff_instance_created = cls.objects.get_or_create(email__iexact=rqst_usr_email,
                                                                       defaults=usr_rqst_values)
    if not staff_instance_created:
        rqst_errors.append('Staff database entry already exists for the email: {!s}'.format(rqst_usr_email))
        staff_instance = None
    else:
        staff_instance.base_locations = validated_params['base_location_objects']
        staff_instance.save()

    return staff_instance


def modify_staff_row_using_validated_params(cls, validated_params, rqst_errors):
    rqst_usr_id = validated_params['rqst_usr_id']

    try:
        staff_instance = cls.objects.get(id=rqst_usr_id)

        if 'rqst_usr_f_name' in validated_params:
            staff_instance.first_name = validated_params['rqst_usr_f_name']

        if 'rqst_usr_l_name' in validated_params:
            staff_instance.last_name = validated_params['rqst_usr_l_name']

        if 'rqst_usr_type' in validated_params:
            staff_instance.type = validated_params['rqst_usr_type']

        if 'rqst_county' in validated_params:
            staff_instance.county = validated_params['rqst_county']

        if 'rqst_usr_email' in validated_params:
            rqst_usr_email = validated_params['rqst_usr_email']
            staff_instance.email = rqst_usr_email
        else:
            rqst_usr_email = staff_instance.email

        if 'base_location_objects' in validated_params:
            staff_instance.base_locations.clear()
            staff_instance.base_locations = validated_params['base_location_objects']

        staff_instance.save()
    except cls.DoesNotExist:
        rqst_errors.append('Staff database entry does not exist for the id: {!s}'.format(str(rqst_usr_id)))
        staff_instance = None
    except cls.MultipleObjectsReturned:
        rqst_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_usr_id)))
        staff_instance = None
    except IntegrityError:
        rqst_errors.append('Database entry already exists for the email: {!s}'.format(rqst_usr_email))
        staff_instance = None

    return staff_instance


def delete_staff_row_using_validated_params(cls, rqst_usr_id, post_errors):
    try:
        staff_instance = cls.objects.get(id=rqst_usr_id)
        staff_instance.delete()
    except cls.DoesNotExist:
        post_errors.append('Staff database entry does not exist for the id: {!s}'.format(str(rqst_usr_id)))
    except cls.MultipleObjectsReturned:
        post_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_usr_id)))
