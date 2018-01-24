from django.db import IntegrityError
from picmodels.models import Address
from picmodels.models import NavMetricsLocation


def get_or_create_address_row(validated_rqst_params):
    default_row_field_values = {
        "address_line_1": validated_rqst_params['rqst_address_line_1'],
        "address_line_2": validated_rqst_params['rqst_address_line_2'],
        "city": validated_rqst_params['rqst_city'],
        "state_province": validated_rqst_params['rqst_state']
    }

    address_instance, address_instance_created = Address.objects.get_or_create(
        defaults=default_row_field_values,
        address_line_1__iexact=validated_rqst_params['rqst_address_line_1'],
        address_line_2__iexact=validated_rqst_params['rqst_address_line_2'],
        city__iexact=validated_rqst_params['rqst_city'],
        state_province__iexact=validated_rqst_params['rqst_state'],
        zipcode=validated_rqst_params['rqst_zipcode'],
        country=validated_rqst_params['country_row']
    )

    return address_instance, address_instance_created


def add_instance_using_validated_params(validated_rqst_params, post_errors):
    address_instance, address_instance_created = get_or_create_address_row(validated_rqst_params)

    try:
        location_instance = NavMetricsLocation(name=validated_rqst_params['rqst_location_name'],
                                               address=address_instance,
                                               cps_location=validated_rqst_params['rqst_cps_location'])
        location_instance.save()
    except IntegrityError:
        location_instance = None
        post_errors.append('Database entry already exists for the name: {} and address: {}'.format(validated_rqst_params['rqst_location_name'],
                                                                                                   address_instance.return_values_dict()))

    return location_instance


def modify_instance_using_validated_params(rqst_location_id, validated_rqst_params, post_errors):
    address_instance, address_instance_created = get_or_create_address_row(validated_rqst_params)

    try:
        location_instance = NavMetricsLocation.objects.get(id=rqst_location_id)
    except NavMetricsLocation.DoesNotExist:
        location_instance = None
        post_errors.append('Nav Hub Location database entry does not exist for the id: {}'.format(rqst_location_id))

    if location_instance:
        location_instance.name = validated_rqst_params['rqst_location_name']
        location_instance.cps_location = validated_rqst_params['rqst_cps_location']
        location_instance.address = address_instance
        try:
            location_instance.save()
        except IntegrityError:
            post_errors.append('Database entry already exists for the name: {} and address: {}'.format(validated_rqst_params['rqst_location_name'],
                                                                                                       address_instance.return_values_dict()))

    return location_instance


def delete_instance_using_validated_params(rqst_location_id, post_errors):
    try:
        location_instance = NavMetricsLocation.objects.get(id=rqst_location_id)
        location_instance.delete()
    except NavMetricsLocation.DoesNotExist:
        post_errors.append('Location database entry does not exist for the id: {!s}'.format(str(rqst_location_id)))
