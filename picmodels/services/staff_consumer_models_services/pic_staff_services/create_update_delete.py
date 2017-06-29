from picmodels.models import PICStaff
from django.db import IntegrityError


def add_instance_using_validated_params(add_staff_params, post_errors):
    staff_instance = create_staff_obj(add_staff_params, post_errors)

    if post_errors:
        staff_instance = None

    return staff_instance


def create_staff_obj(staff_params, rqst_errors):
    rqst_usr_email = staff_params['rqst_usr_email']
    usr_rqst_values = {"first_name": staff_params['rqst_usr_f_name'],
                       "last_name": staff_params['rqst_usr_l_name'],
                       "type": staff_params['rqst_usr_type'],
                       "county": staff_params['rqst_county'],
                       "mpn": staff_params['rqst_usr_mpn']}
    staff_instance, staff_instance_created = PICStaff.objects.get_or_create(email=rqst_usr_email,
                                                                            defaults=usr_rqst_values)
    if not staff_instance_created:
        rqst_errors.append('Staff database entry already exists for the email: {!s}'.format(rqst_usr_email))
    else:
        staff_instance.base_locations = staff_params['base_location_objects']
        staff_instance.save()

    return staff_instance


def modify_instance_using_validated_params(modify_staff_params, post_errors):
    staff_instance = modify_staff_obj(modify_staff_params, post_errors)

    return staff_instance


def modify_staff_obj(staff_params, rqst_errors):
    rqst_usr_email = staff_params['rqst_usr_email']
    rqst_usr_id = staff_params['rqst_usr_id']

    try:
        staff_instance = PICStaff.objects.get(id=rqst_usr_id)
        staff_instance.first_name = staff_params['rqst_usr_f_name']
        staff_instance.last_name = staff_params['rqst_usr_l_name']
        staff_instance.type = staff_params['rqst_usr_type']
        staff_instance.county = staff_params['rqst_county']
        staff_instance.email = rqst_usr_email
        staff_instance.mpn = staff_params['rqst_usr_mpn']

        staff_instance.base_locations.clear()
        staff_instance.base_locations = staff_params['base_location_objects']

        staff_instance.save()
    except PICStaff.DoesNotExist:
        rqst_errors.append('Staff database entry does not exist for the id: {!s}'.format(str(rqst_usr_id)))
        staff_instance = None
    except PICStaff.MultipleObjectsReturned:
        rqst_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_usr_id)))
        staff_instance = None
    except IntegrityError:
        rqst_errors.append('Database entry already exists for the email: {!s}'.format(rqst_usr_email))
        staff_instance = None

    return staff_instance


def delete_instance_using_validated_params(rqst_usr_id, post_errors):
    try:
        staff_instance = PICStaff.objects.get(id=rqst_usr_id)
        staff_instance.delete()
    except PICStaff.DoesNotExist:
        post_errors.append('Staff database entry does not exist for the id: {!s}'.format(str(rqst_usr_id)))
    except PICStaff.MultipleObjectsReturned:
        post_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_usr_id)))
