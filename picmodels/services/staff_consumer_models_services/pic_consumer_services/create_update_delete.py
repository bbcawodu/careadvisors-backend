import json
from picmodels.models import PICConsumer
from picmodels.models import PICConsumerBackup
from picmodels.models import ConsumerNote
from picmodels.models import Address
from picmodels.models import Country
from picmodels.models import ConsumerCPSInfoEntry
from picmodels.models import NavMetricsLocation
from django.db import IntegrityError


def add_instance_using_validated_params(add_consumer_params, post_errors):
    consumer_instance = None
    backup_consumer_obj = None
    matching_consumer_instances = None

    found_consumers = PICConsumer.objects.filter(first_name=add_consumer_params['rqst_consumer_f_name'],
                                                 last_name=add_consumer_params['rqst_consumer_l_name'])
    if found_consumers and not add_consumer_params['force_create_consumer']:
        query_params = {"first_name": add_consumer_params['rqst_consumer_f_name'],
                        "last_name": add_consumer_params['rqst_consumer_l_name'], }
        post_errors.append('Consumer database entry(s) already exists for the parameters: {!s}'.format(
            json.dumps(query_params)))
        matching_consumer_instances = found_consumers.all()
    else:
        consumer_instance, backup_consumer_obj = create_consumer_obj(add_consumer_params, post_errors)

    return matching_consumer_instances, consumer_instance, backup_consumer_obj


def create_consumer_obj(consumer_params, post_errors):
    address_instance = None
    if consumer_params['rqst_address_line_1'] != '' and consumer_params['rqst_city'] != '' and \
                    consumer_params['rqst_state'] != '' and consumer_params['rqst_zipcode'] != '':
        address_instance, address_instance_created = Address.objects.get_or_create(
            address_line_1=consumer_params['rqst_address_line_1'],
            address_line_2=consumer_params['rqst_address_line_2'],
            city=consumer_params['rqst_city'],
            state_province=consumer_params['rqst_state'],
            zipcode=consumer_params['rqst_zipcode'],
            country=Country.objects.all()[0])

    backup_consumer_obj = None

    nav_instance = consumer_params['nav_instance']
    consumer_instance = PICConsumer(first_name=consumer_params['rqst_consumer_f_name'],
                                    middle_name=consumer_params['rqst_consumer_m_name'],
                                    last_name=consumer_params['rqst_consumer_l_name'],
                                    email=consumer_params['rqst_consumer_email'],
                                    phone=consumer_params['rqst_consumer_phone'],
                                    plan=consumer_params['rqst_consumer_plan'],
                                    preferred_language=consumer_params['rqst_consumer_pref_lang'],
                                    address=address_instance,
                                    date_met_nav=consumer_params['rqst_date_met_nav'],
                                    met_nav_at=consumer_params['rqst_consumer_met_nav_at'],
                                    household_size=consumer_params['rqst_consumer_household_size'],
                                    )
    consumer_instance.navigator = nav_instance
    consumer_instance.save()

    for navigator_note in consumer_params['rqst_navigator_notes']:
        consumer_note_object = ConsumerNote(consumer=consumer_instance,
                                            navigator_notes=navigator_note)
        consumer_note_object.save()

    if consumer_params['rqst_cps_consumer']:
        add_cps_info_to_consumer_instance(consumer_instance, consumer_params['validated_cps_info_dict'], post_errors)

    if not post_errors and consumer_params['rqst_create_backup']:
        backup_consumer_obj = create_backup_consumer_obj(consumer_instance)

    return consumer_instance, backup_consumer_obj


def add_cps_info_to_consumer_instance(consumer_instance, validated_cps_info_params, post_errors):
    """
    This function takes a consumer database instance and a dictionary populated with CPS consumer info, parses the info
    for errors, and adds the CPS to the consumer info if there are no errors.

    :param consumer_instance: (type: PICConsumer) PICConsumer instance to add CPS info to
    :param rqst_cps_info_dict: (type: dictionary) CPS info to parse
    :param post_errors: (type: list) list of error messages
    :return: None
    """

    cps_info_object = ConsumerCPSInfoEntry()

    rqst_cps_location = validated_cps_info_params["rqst_cps_location"]
    try:
        cps_location_object = NavMetricsLocation.objects.get(name=rqst_cps_location)
        if not cps_location_object.cps_location:
            post_errors.append("{!s} is not a cps_location".format(rqst_cps_location))
        else:
            cps_info_object.cps_location = cps_location_object
    except NavMetricsLocation.DoesNotExist:
        post_errors.append("NavMetricsLocation object does not exist for name: {!s}".format(rqst_cps_location))

    cps_info_object.apt_date = validated_cps_info_params["rqst_apt_date"]
    cps_info_object.target_list = validated_cps_info_params["rqst_target_list"]
    cps_info_object.phone_apt = validated_cps_info_params["rqst_phone_apt"]
    cps_info_object.case_mgmt_type = validated_cps_info_params["rqst_case_mgmt_type"]

    cps_info_object.case_mgmt_status = validated_cps_info_params["rqst_case_mgmt_status"]
    if not cps_info_object.check_case_mgmt_status_choices():
        post_errors.append("case_mgmt_status: {!s} is not a valid choice".format(cps_info_object.case_mgmt_status))
    cps_info_object.app_type = validated_cps_info_params["rqst_app_type"]
    if not cps_info_object.check_app_type_choices():
        post_errors.append("app_type: {!s} is not a valid choice".format(cps_info_object.app_type))
    cps_info_object.app_status = validated_cps_info_params["rqst_app_status"]
    if not cps_info_object.check_app_status_choices():
        post_errors.append("app_status: {!s} is not a valid choice".format(cps_info_object.app_status))

    if not post_errors:
        consumer_instance.cps_consumer = True
        consumer_instance.save()

        primary_dependent_object = validated_cps_info_params["primary_dependent_object"]
        if primary_dependent_object._state.adding:
            primary_dependent_object.save()
        cps_info_object.primary_dependent = primary_dependent_object
        cps_info_object.save()

        secondary_dependents_list = validated_cps_info_params["secondary_dependents_list"]
        if secondary_dependents_list:
            for secondary_dependent_instance in secondary_dependents_list:
                if secondary_dependent_instance._state.adding:
                    secondary_dependent_instance.save()
            cps_info_object.secondary_dependents = secondary_dependents_list
        cps_info_object.save()

        consumer_instance.cps_info = cps_info_object
        consumer_instance.save()
    else:
        consumer_instance.delete()


# getattr(object, field_name)
# need to manually copy consumer notes
def create_backup_consumer_obj(consumer_instance):
    """
    This function takes a PICConsumer instance, creates a PICConsumerBackup instance with the same information as the
    given PICConsumer instance and returns the PICConsumerBackup instance.

    :param consumer_instance: (type: PICConsumer) PICConsumer instance to be copied
    :return: (type: PICConsumerBackup) copied PICConsumerBackup instance
    """

    consumer_instance_fields = consumer_instance._meta.get_fields()
    non_null_field_name_list = []
    for field in consumer_instance_fields:
        try:
            if getattr(consumer_instance, field.name) is not None and field.name != 'id':
                non_null_field_name_list.append(field.name)
        except AttributeError:
            pass

    backup_consumer_obj = PICConsumerBackup()
    for orig_field in non_null_field_name_list:
        orig_field_value = getattr(consumer_instance, orig_field)
        if orig_field == "cps_info":
            pass
        else:
            setattr(backup_consumer_obj, orig_field, orig_field_value)
    backup_consumer_obj.save()

    if "cps_info" in non_null_field_name_list:
        cps_info_copy = ConsumerCPSInfoEntry()
        cps_info_orig = getattr(consumer_instance, "cps_info")
        cps_info_orig_fields = cps_info_orig._meta.get_fields()

        for cps_info_orig_field in cps_info_orig_fields:
            try:
                cps_info_orig_field_value = getattr(cps_info_orig, cps_info_orig_field.name)

                if cps_info_orig_field.name == 'secondary_dependents':
                    # Need to implement something to copy secondary dependents, breaks if you omit this
                    pass
                elif cps_info_orig_field.name != 'id':
                    setattr(cps_info_copy, cps_info_orig_field.name, cps_info_orig_field_value)
            except AttributeError:
                pass
        cps_info_copy.save()

        setattr(backup_consumer_obj, "cps_info", cps_info_copy)
        backup_consumer_obj.save()

    orig_consumer_notes = ConsumerNote.objects.filter(consumer=consumer_instance.id)
    for consumer_note in orig_consumer_notes:
        consumer_note_copy_object = ConsumerNote(consumer_backup=backup_consumer_obj,
                                                 navigator_notes=consumer_note.navigator_notes)
        consumer_note_copy_object.save()

    return backup_consumer_obj


def modify_instance_using_validated_params(modify_consumer_params, post_errors):
    consumer_instance, backup_consumer_obj = modify_consumer_obj(modify_consumer_params, post_errors)

    return consumer_instance, backup_consumer_obj


def modify_consumer_obj(consumer_params, post_errors):
    consumer_instance = None
    backup_consumer_obj = None

    address_instance = None
    if consumer_params['rqst_address_line_1'] != '' and consumer_params['rqst_city'] != '' and \
                    consumer_params['rqst_state'] != '' and consumer_params['rqst_zipcode'] != '':
        address_instance, address_instance_created = Address.objects.get_or_create(
            address_line_1=consumer_params['rqst_address_line_1'],
            address_line_2=consumer_params['rqst_address_line_2'],
            city=consumer_params['rqst_city'],
            state_province=consumer_params['rqst_state'],
            zipcode=consumer_params['rqst_zipcode'],
            country=Country.objects.all()[0])

    try:
        consumer_instance = PICConsumer.objects.get(id=consumer_params['rqst_consumer_id'])
        consumer_instance.first_name = consumer_params['rqst_consumer_f_name']
        consumer_instance.middle_name = consumer_params['rqst_consumer_m_name']
        consumer_instance.last_name = consumer_params['rqst_consumer_l_name']
        consumer_instance.phone = consumer_params['rqst_consumer_phone']
        consumer_instance.address = address_instance
        consumer_instance.plan = consumer_params['rqst_consumer_plan']
        consumer_instance.met_nav_at = consumer_params['rqst_consumer_met_nav_at']
        consumer_instance.household_size = consumer_params['rqst_consumer_household_size']
        consumer_instance.preferred_language = consumer_params['rqst_consumer_pref_lang']
        consumer_instance.email = consumer_params['rqst_consumer_email']
        consumer_instance.date_met_nav = consumer_params['rqst_date_met_nav']
        consumer_instance.navigator = consumer_params['nav_instance']

        if consumer_params['rqst_cps_consumer'] is not None:
            consumer_instance.cps_consumer = consumer_params['rqst_cps_consumer']
            if consumer_params['rqst_cps_consumer']:
                modify_consumer_cps_info(consumer_instance, consumer_params['validated_cps_info_dict'], post_errors)
            else:
                try:
                    consumer_cps_info = consumer_instance.cps_info
                    consumer_instance.cps_info.remove()
                    consumer_cps_info.delete()
                except ConsumerCPSInfoEntry.DoesNotExist:
                    pass
        else:
            pass

        if len(post_errors) == 0:
            consumer_instance.save()
            old_consumer_notes = ConsumerNote.objects.filter(consumer=consumer_instance.id)
            for old_consumer_note in old_consumer_notes:
                old_consumer_note.delete()

            for navigator_note in consumer_params['rqst_navigator_notes']:
                consumer_note_object = ConsumerNote(consumer=consumer_instance, navigator_notes=navigator_note)
                consumer_note_object.save()

            if consumer_params['rqst_create_backup']:
                backup_consumer_obj = create_backup_consumer_obj(consumer_instance)
    except PICConsumer.DoesNotExist:
        post_errors.append('Consumer database entry does not exist for the id: {!s}'.format(
            str(consumer_params['rqst_consumer_id'])))
    except PICConsumer.MultipleObjectsReturned:
        post_errors.append(
            'Multiple database entries exist for the id: {!s}'.format(str(consumer_params['rqst_consumer_id'])))
    except IntegrityError:
        post_errors.append(
            'Database entry already exists for the id: {!s}'.format(str(consumer_params['rqst_consumer_id'])))

    return consumer_instance, backup_consumer_obj


def modify_consumer_cps_info(consumer_instance, validated_cps_info_params, post_errors):
    """
    This function takes a consumer database instance and a dictionary populated with CPS consumer info, parses the info
    for errors, and modifies the CPS info for that consumer if there are no errors.

    :param consumer_instance: (type: PICConsumer) PICConsumer instance to add CPS info to
    :param rqst_cps_info_dict: (type: dictionary) CPS info to parse
    :param post_errors: (type: list) list of error messages
    :return: None
    """

    try:
        cps_info_object = consumer_instance.cps_info
    except ConsumerCPSInfoEntry.DoesNotExist:
        cps_info_object = ConsumerCPSInfoEntry()

    rqst_cps_location = validated_cps_info_params["rqst_cps_location"]
    try:
        cps_location_object = NavMetricsLocation.objects.get(name=rqst_cps_location)
        if not cps_location_object.cps_location:
            post_errors.append("{!s} is not a cps_location".format(rqst_cps_location))
        else:
            cps_info_object.cps_location = cps_location_object
    except NavMetricsLocation.DoesNotExist:
        post_errors.append("NavMetricsLocation object does not exist for name: {!s}".format(rqst_cps_location))

    cps_info_object.apt_date = validated_cps_info_params['rqst_apt_date']
    cps_info_object.target_list = validated_cps_info_params['rqst_target_list']
    cps_info_object.phone_apt = validated_cps_info_params['rqst_phone_apt']
    cps_info_object.case_mgmt_type = validated_cps_info_params['rqst_case_mgmt_type']

    cps_info_object.case_mgmt_status = validated_cps_info_params['rqst_case_mgmt_status']
    if not cps_info_object.check_case_mgmt_status_choices():
        post_errors.append("case_mgmt_status: {!s} is not a valid choice".format(cps_info_object.case_mgmt_status))
    cps_info_object.app_type = validated_cps_info_params['rqst_app_type']
    if not cps_info_object.check_app_type_choices():
        post_errors.append("app_type: {!s} is not a valid choice".format(cps_info_object.app_type))
    cps_info_object.app_status = validated_cps_info_params['rqst_app_status']
    if not cps_info_object.check_app_status_choices():
        post_errors.append("app_status: {!s} is not a valid choice".format(cps_info_object.app_status))

    if len(post_errors) == 0:
        consumer_instance.cps_consumer = True
        consumer_instance.save()

        primary_dependent_object = validated_cps_info_params['primary_dependent_object']
        if primary_dependent_object._state.adding:
            primary_dependent_object.save()
        cps_info_object.primary_dependent = primary_dependent_object

        cps_info_object.save()

        secondary_dependents_list = validated_cps_info_params['secondary_dependents_list']
        if cps_info_object.secondary_dependents:
            cps_info_object.secondary_dependents.clear()
        if secondary_dependents_list:
            for secondary_dependent_instance in secondary_dependents_list:
                if secondary_dependent_instance._state.adding:
                    secondary_dependent_instance.save()
            cps_info_object.secondary_dependents = secondary_dependents_list

        cps_info_object.save()

        consumer_instance.cps_info = cps_info_object
        consumer_instance.save()


def delete_instance_using_validated_params(rqst_consumer_id, rqst_create_backup, post_errors):
    backup_consumer_obj = None

    try:
        consumer_instance = PICConsumer.objects.get(id=rqst_consumer_id)

        if rqst_create_backup:
            backup_consumer_obj = create_backup_consumer_obj(consumer_instance)

        consumer_instance.delete()
    except PICConsumer.DoesNotExist:
        post_errors.append('Consumer database entry does not exist for the id: {}'.format(rqst_consumer_id))

    return backup_consumer_obj
