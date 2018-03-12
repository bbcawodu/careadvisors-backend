from django.db import IntegrityError
import picmodels


def create_row_w_validated_params(cls, validated_params, rqst_errors):
    address_instance, address_instance_created = get_or_create_address_row(validated_params)

    try:
        location_instance = cls(
            name=validated_params['rqst_location_name'],
            address=address_instance,
            cps_location=validated_params['rqst_cps_location']
        )
        location_instance.save()
    except IntegrityError:
        location_instance = None
        rqst_errors.append(
            'Database entry already exists for the name: {} and address: {}'.format(
                validated_params['rqst_location_name'],
                address_instance.return_values_dict()
            )
        )

    return location_instance


def update_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['rqst_id']
    address_instance, address_instance_created = get_or_create_address_row(validated_params)

    try:
        location_instance = cls.objects.get(id=rqst_id)
    except cls.DoesNotExist:
        location_instance = None
        rqst_errors.append('Nav Hub Location database entry does not exist for the id: {}'.format(rqst_id))

    if location_instance:
        if 'rqst_location_name' in validated_params:
            location_instance.name = validated_params['rqst_location_name']
        if 'rqst_cps_location' in validated_params:
            location_instance.cps_location = validated_params['rqst_cps_location']

        location_instance.address = address_instance

        try:
            location_instance.save()
        except IntegrityError:
            rqst_errors.append(
                'Database entry already exists for the name: {} and address: {}'.format(
                    validated_params['rqst_location_name'],
                    address_instance.return_values_dict()
                )
            )

    return location_instance


def delete_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['rqst_id']

    try:
        location_instance = cls.objects.get(id=rqst_id)
        location_instance.delete()
    except cls.DoesNotExist:
        rqst_errors.append('Location database entry does not exist for the id: {!s}'.format(str(rqst_id)))


def get_or_create_address_row(validated_params):
    default_row_field_values = {
        "address_line_1": validated_params['rqst_address_line_1'],
        "address_line_2": validated_params['rqst_address_line_2'],
        "city": validated_params['rqst_city'],
        "state_province": validated_params['rqst_state']
    }

    address_instance, address_instance_created = picmodels.models.Address.objects.get_or_create(
        defaults=default_row_field_values,
        address_line_1__iexact=validated_params['rqst_address_line_1'],
        address_line_2__iexact=validated_params['rqst_address_line_2'],
        city__iexact=validated_params['rqst_city'],
        state_province__iexact=validated_params['rqst_state'],
        zipcode=validated_params['rqst_zipcode'],
        country=validated_params['country_row']
    )

    return address_instance, address_instance_created
